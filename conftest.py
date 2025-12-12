import logging
import os
import subprocess
from datetime import datetime
from io import BytesIO
from typing import List, Callable

import allure
import pytest
from PIL import Image
from _pytest.fixtures import FixtureRequest
from appium import webdriver
from loguru import logger

from pages.bookshelf_app.bookshelf_page import BookshelfPage
from pages.cloud_sort_page import CloudSortPage
from pages.clouds_more_page import CloudsMorePage
from pages.home_clouds_page import HomeCloudsPage
from pages.nut_cloud_page.account_information_page import AccountInformationPage
from pages.nut_cloud_page.details_page import DetailsPage
from pages.nut_cloud_page.document_home_page import DocumentHomePage
from pages.nut_cloud_page.file_page import FilePage
from pages.nut_cloud_page.home_page import HomePage
from pages.nut_cloud_page.nut_login_page import NutLoginPage
from utils.app_switcher import AppSwitcher
# 从配置模块导入
from utils.driver import init_driver
from utils.test_data_loader import load_test_data

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
folder_list = load_test_data("enter_folder_list.json")
# 全局配置
SCREENSHOT_DIR = os.path.join(BASE_DIR, "reports", "screenshots")
ALLURE_RESULTS_DIR = os.path.join(BASE_DIR, "allure-results")
MAX_RECORDINGS = 100  # 最大录制文件数
GLOBAL_LOG_DIR = os.path.join(BASE_DIR, "logs", "pytest_runs")
# 初始化日志
logger = logging.getLogger(__name__)


def custom_log_namer(default_name):
    base, ext = os.path.splitext(default_name)
    if not ext:  # 如果默认没有扩展名
        return default_name
    
    # 分离基础名和日期部分
    parts = base.split('.')
    if len(parts) > 1:
        # 格式化为 pytest_2025-08-05.log
        date_part = parts[-1]
        base_name = '.'.join(parts[:-1])
        return f"{base_name}_{date_part}.log"
    return default_name


def pytest_configure(config):
    """配置测试环境"""
    # 生成带时间戳的日志文件名
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file_name = f"pytest_run_{timestamp}.log"
    log_file_path = os.path.join(GLOBAL_LOG_DIR, log_file_name)
    # 强制日志文件为绝对路径（避免pytest内部处理相对路径）
    log_file_path = os.path.abspath(log_file_path)
    config.option.log_file = log_file_path
    # 确保所有目录存在（覆盖所有可能的目录）
    for dir_path in [SCREENSHOT_DIR, ALLURE_RESULTS_DIR, GLOBAL_LOG_DIR]:
        os.makedirs(dir_path, exist_ok=True)
        # 再次验证目录是否存在（调试用）
        if not os.path.exists(dir_path):
            logger.warning(f"目录创建失败: {dir_path}")
    # 动态设置本次运行的日志文件路径
    # 关键：这将覆盖 pytest.ini 或命令行中指定的 log_file 设置
    config.option.allure_report_dir = ALLURE_RESULTS_DIR
    
    # （可选）同时配置 log_cli 如果你想在控制台也看到实时日志
    # config.option.log_cli = True
    # config.option.log_cli_level = 'INFO'
    
    # 确保其他目录存在
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    os.makedirs(ALLURE_RESULTS_DIR, exist_ok=True)
    # 设置 Allure 结果目录
    config.option.allure_report_dir = ALLURE_RESULTS_DIR
    # 清理旧文件（可选，现在针对的是全局日志目录）
    cleanup_old_files(GLOBAL_LOG_DIR, ['.log'], MAX_RECORDINGS)
    cleanup_old_files(SCREENSHOT_DIR, ['.png'], MAX_RECORDINGS)
    
    logger.info(f"本次测试运行日志将保存至: {log_file_path}")


def cleanup_old_files(directory, extensions, max_files):
    """清理旧文件，保留最新的 max_files 个指定扩展名的文件"""
    if not os.path.exists(directory):
        return
    
    try:
        # 获取所有指定扩展名的文件并按修改时间排序
        files = []
        for f in os.listdir(directory):
            if any(f.lower().endswith(ext) for ext in extensions):
                file_path = os.path.join(directory, f)
                if os.path.isfile(file_path):
                    files.append(file_path)
        
        files = sorted(files, key=os.path.getmtime, reverse=True)
        
        # 删除超出保留数量的旧文件
        for old_file in files[max_files:]:
            try:
                os.remove(old_file)
                logger.info(f"已删除旧文件: {os.path.basename(old_file)}")
            except Exception as e:
                logger.warning(f"删除文件失败: {e}")
    except Exception as e:
        logger.error(f"清理文件时发生错误: {e}")


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """处理测试报告生成"""
    # 获取测试结果
    outcome = yield
    report = outcome.get_result()
    
    # 只在测试失败时处理（包括setup, call, teardown阶段）
    if report.failed:
        # 查找driver实例 - 从多个地方查找
        driver = None
        
        # 1. 首先尝试从fixture参数中查找
        for fixture_name in item.funcargs:
            fixture = item.funcargs[fixture_name]
            if hasattr(fixture, 'driver') and isinstance(fixture.driver, webdriver.Remote):
                driver = fixture.driver
                break
            elif isinstance(fixture, webdriver.Remote):
                driver = fixture
                break
        
        # 2. 如果没找到，尝试从item的config中查找
        if driver is None and hasattr(item.config, 'driver'):
            driver = item.config.driver
        
        # 3. 如果还没找到，尝试从模块或类属性中查找
        if driver is None and hasattr(item, 'instance') and hasattr(item.instance, 'driver'):
            driver = item.instance.driver
        
        if driver:
            try:
                # 生成截图名称
                test_name = item.nodeid.replace("::", "_").replace("/", "_").replace(".", "_")[:100]
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                screenshot_name = f"FAIL_{report.when.upper()}_{test_name}_{timestamp}.png"
                screenshot_path = os.path.join(SCREENSHOT_DIR, screenshot_name)
                
                # 保存截图
                driver.save_screenshot(screenshot_path)
                logger.info(f"测试失败截图已保存: {screenshot_name}")
                
                # 附加到Allure报告
                allure.attach.file(
                    screenshot_path,
                    name=f"{report.when.capitalize()}阶段失败截图: {item.name}",
                    attachment_type=allure.attachment_type.PNG
                )
                
                # 为pytest-html报告准备数据
                if hasattr(report, "extra"):
                    # 获取HTML报告插件
                    html = item.config.pluginmanager.getplugin("html")
                    if html:
                        # 添加缩略图
                        try:
                            with open(screenshot_path, "rb") as f:
                                img = Image.open(f)
                                img.thumbnail((400, 400))  # 创建缩略图
                                img_bytes = BytesIO()
                                img.save(img_bytes, format='PNG')
                                img_bytes = img_bytes.getvalue()
                            
                            # 创建相对路径用于HTML报告
                            if hasattr(item.config.option, 'htmlpath') and item.config.option.htmlpath:
                                rel_path = os.path.relpath(screenshot_path,
                                                           os.path.dirname(item.config.option.htmlpath))
                            else:
                                # 如果没有设置 htmlpath，使用绝对路径或默认路径
                                rel_path = screenshot_path
                            # 添加到报告extra
                            report.extra = getattr(report, "extra", []) + [
                                html.extras.image(img_bytes, "缩略图"),
                                html.extras.html(f'<div><a href="{rel_path}" target="_blank">'
                                                 f'<img src="{rel_path}" width="400"></a></div>')
                            ]
                        except Exception as e:
                            logger.error(f"处理截图缩略图失败: {e}", exc_info=True)
            except Exception as e:
                logger.error(f"截图保存失败: {e}", exc_info=True)
        else:
            logger.warning(f"未找到可用的driver实例，无法为失败测试截图: {item.nodeid}")
    
    # 处理录制的视频 - 无论测试是否失败都附加视频
    if hasattr(item, 'video_path') and os.path.exists(item.video_path):
        try:
            # 附加到Allure报告
            allure.attach.file(
                item.video_path,
                name=f"{report.when.capitalize()}阶段录屏: {item.name}",
                attachment_type=allure.attachment_type.MP4
            )
            logger.info(f"已将录屏附加到Allure报告: {os.path.basename(item.video_path)}")
            
            # 为pytest-html报告添加视频链接
            if hasattr(report, "extra") and report.when == "call":
                html = item.config.pluginmanager.getplugin("html")
                if html:
                    # 创建相对路径
                    rel_video_path = os.path.relpath(item.video_path, os.path.dirname(item.config.option.htmlpath))
                    
                    # 添加视频链接
                    report.extra = getattr(report, "extra", []) + [
                        html.extras.html(f'<div><a href="{rel_video_path}" target="_blank">'
                                         f'查看测试录屏: {os.path.basename(item.video_path)}</a></div>')
                    ]
        except Exception as e:
            logger.error(f"附加录屏到报告失败: {e}", exc_info=True)


def pytest_html_report_title(report):
    """设置HTML报告标题"""
    report.title = f"自动化测试报告 - {datetime.now().strftime('%Y-%m-%d')}"


def pytest_html_results_summary(prefix, summary, postfix):
    """在HTML报告中添加总结信息"""
    prefix.extend([
        f"<p>测试时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>",
        f"<p>测试环境: {os.environ.get('TEST_ENV', '未指定')}</p>",
        f"<p>录屏功能: {'启用' if os.environ.get('ENABLE_RECORDING', 'true').lower() == 'true' else '禁用'}</p>"
    ])


# 添加session级别的teardown
def pytest_sessionfinish(session, exitstatus):
    """测试会话结束时执行"""
    logger.info("=" * 50)
    logger.info(f"测试会话结束状态: {exitstatus}")
    logger.info("=" * 50)


def clean_database(device_id=None):
    """清理数据库文件，如果文件不存在则记录日志"""
    db_path = "/storage/emulated/0/hwsys/database/clouds.db"
    adb_prefix = f"adb -s {device_id}" if device_id else "adb"
    
    # 1. 检查文件是否存在
    check_cmd = f"{adb_prefix} shell ls {db_path}"
    check_result = subprocess.run(
        check_cmd,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # 2. 根据存在性执行不同操作
    if check_result.returncode == 0:
        # 文件存在 - 执行删除
        del_cmd = f"{adb_prefix} shell rm -f {db_path}"
        del_result = subprocess.run(
            del_cmd,
            shell=True,
            capture_output=True,
            text=True
        )
        
        if del_result.returncode == 0:
            logger.info(f"✅ 成功删除数据库文件: {db_path}")
        else:
            logger.error(f"❌ 删除数据库文件失败: {del_result.stderr.strip()}")
            pytest.fail(f"数据库文件删除失败: {del_result.stderr.strip()}")
    else:
        # 文件不存在 - 记录信息日志
        logger.info(f"ℹ️ 数据库文件不存在，无需删除: {db_path}")
        # 检查错误是否是"文件不存在"（避免漏报其他错误）
        if "No such file or directory" not in check_result.stderr:
            logger.warning(f"⚠️ 文件检查异常: {check_result.stderr.strip()}")


class CleanupManager:
    def __init__(self):
        self.cleanup_actions: List[Callable] = []
        self.skip_default_cleanup = False
    
    def register_cleanup(self, func: Callable):
        """注册清理函数"""
        self.cleanup_actions.append(func)
    
    def set_skip_default_cleanup(self):
        """设置跳过默认清理"""
        self.skip_default_cleanup = True
    
    def execute_cleanup(self):
        """执行所有注册的清理操作"""
        # 执行所有自定义清理操作
        for cleanup_action in self.cleanup_actions:
            try:
                cleanup_action()
            except Exception as e:
                logger.error(f"清理动作执行失败: {str(e)}")
                # 可以选择是否让测试失败
                # pytest.fail(f"清理动作执行失败: {str(e)}")
        
        # 返回是否需要执行默认清理
        return not self.skip_default_cleanup


@pytest.fixture(scope="function")
def cleanup_manager():
    manager = CleanupManager()
    yield manager
    # 在测试结束后执行所有注册的清理操作，但不管默认清理（默认清理由各个fixture自己处理）
    manager.execute_cleanup()  # 注意：这个方法现在只执行注册的清理，不处理默认清理


@pytest.fixture(scope="session")
def app_driver(request):
    # 获取命令行参数
    device_id = request.config.getoption("--device-id", default=None)
    app_package = request.config.getoption("--app-package", default="com.example.app")
    app_activity = request.config.getoption("--app-activity", default=".MainActivity")
    
    # 执行智能清理，下方注释打开后每一次都会执行清空数据库操作
    # clean_database(device_id)
    """创建并返回Appium driver"""
    driver = init_driver()
    yield driver
    driver.quit()


@pytest.fixture(scope="function")
def app_switcher(app_driver):
    """应用切换工具类的 fixture"""
    return AppSwitcher(app_driver)


# 3. 👇 新增：页面夹具（创建 DocumentHomePage 实例，传入 driver 和 app_info）
@pytest.fixture(scope="module")
def document_home_page(driver):
    # 关键：把 app_info 传入页面类的构造函数
    return DocumentHomePage(driver=driver)


@pytest.fixture(scope="session")
def setup(app_driver):  # 注意：这里移除了self参数
    home_cloud_page = HomeCloudsPage(app_driver)
    yield home_cloud_page


@pytest.fixture(scope="session")
def nut_cloud_logged(setup):
    setup.click_nut_cloud_success()
    yield app_driver


@pytest.fixture(scope="session")
def logged_in_driver(nut_cloud_logged, app_driver):
    """Session 范围的已登录 driver"""
    login_page = NutLoginPage(app_driver)
    login_page.login_successful()
    yield app_driver


@pytest.fixture(scope="function")
def nut_cloud_login_page(logged_in_driver, cleanup_manager):
    home_page = HomePage(logged_in_driver)
    # 将清理方法附加到页面对象上
    home_page.register_cleanup = cleanup_manager.register_cleanup
    home_page.set_skip_default_cleanup = cleanup_manager.set_skip_default_cleanup
    yield home_page
    if not cleanup_manager.skip_default_cleanup:
        try:
            home_page.navigate_back(1)
        except Exception as e:
            logger.info(f"默认清理失败: {e}")


# 获取有效的登录凭证
@pytest.fixture(scope="class")
def logged_in_home_page(app_driver):
    home_page = HomePage(app_driver)
    yield home_page


@pytest.fixture(scope="function")
def logged_in_details_page(logged_in_home_page):
    details_page = DetailsPage(logged_in_home_page.driver)
    logged_in_home_page.long_press_cloud_success()
    yield details_page


@pytest.fixture(scope="function")
def cloud_more_window(logged_in_home_page):
    more_page = CloudsMorePage(logged_in_home_page.driver)
    logged_in_home_page.click_more_button_workflow()
    yield more_page
    more_page.back()


@pytest.fixture(scope="function")
def cloud_sort_button(logged_in_home_page):
    more_page = CloudsMorePage(logged_in_home_page.driver)
    logged_in_home_page.click_more_button_workflow()
    cloud_sort_page = CloudSortPage(logged_in_home_page.driver)
    more_page.click_sort_button_success()
    yield cloud_sort_page


# 获取账户信息页
@pytest.fixture(scope="function")
def logged_in_account_information_page(logged_in_details_page, cleanup_manager):
    account_information_page = AccountInformationPage(logged_in_details_page.driver)
    # 使用新的导航方法
    logged_in_details_page.navigate_to_account_information()
    account_information_page.register_cleanup = cleanup_manager.register_cleanup
    account_information_page.set_skip_default_cleanup = cleanup_manager.set_skip_default_cleanup
    yield account_information_page


@pytest.fixture(scope="function")
def logged_in_account_edit_page(logged_in_account_information_page, cleanup_manager):
    edit_account_modal = logged_in_account_information_page.EditAccountModal(
        logged_in_account_information_page.driver
    )
    edit_account_edit = edit_account_modal.click_edit_button()
    edit_account_edit.register_cleanup = cleanup_manager.register_cleanup
    edit_account_edit.set_skip_default_cleanup = cleanup_manager.set_skip_default_cleanup
    yield edit_account_edit


# 获取重命名页
@pytest.fixture(scope="function")
def logged_in_account_rename_page(logged_in_details_page, logged_in_home_page, cleanup_manager):
    try:
        # 使用新的导航方法
        account_info_page = logged_in_details_page.navigate_to_account_rename()
        account_info_page.register_cleanup = cleanup_manager.register_cleanup
        account_info_page.set_skip_default_cleanup = cleanup_manager.set_skip_default_cleanup
        yield account_info_page
    
    except Exception as e:
        logger.error(f"账户信息页加载失败: {str(e)}")
        pytest.fail(f"无法加载账户信息页: {str(e)}")


@pytest.fixture(scope="function")
def nut_cloud_login(setup, cleanup_manager):
    nut_login_page = NutLoginPage(setup.driver)
    setup.click_nut_cloud_success()
    # 将清理方法附加到页面对象上
    nut_login_page.register_cleanup = cleanup_manager.register_cleanup
    nut_login_page.set_skip_default_cleanup = cleanup_manager.set_skip_default_cleanup
    
    yield nut_login_page
    
    if not cleanup_manager.skip_default_cleanup:
        try:
            nut_login_page.navigate_back(1)
        except Exception as e:
            logger.info(f"默认清理失败: {e}")


@pytest.fixture(scope="session")
def click_nut_cloud(app_driver):
    home_page = HomePage(app_driver)
    home_page.click_cloud()
    yield app_driver


@pytest.fixture(scope="function")
def enter_nut_cloud_home(app_driver, click_nut_cloud, cleanup_manager):
    document_home_page = DocumentHomePage(app_driver)
    document_home_page.register_cleanup = cleanup_manager.register_cleanup
    document_home_page.set_skip_default_cleanup = cleanup_manager.set_skip_default_cleanup
    yield document_home_page
    if not cleanup_manager.skip_default_cleanup:
        try:
            document_home_page.navigate_back(1)
        except Exception as e:
            logger.info(f"默认清理失败: {e}")


@pytest.fixture(scope="package")
def enter_folder_page_parametrized(app_driver, click_nut_cloud):
    """参数化的进入文件夹页面fixture"""
    enter_nut_cloud_home = DocumentHomePage(app_driver)
    enter_nut_cloud_home.enter_file_page(folder_list[0]["filenames"])
    enter_nut_cloud_home.enter_file_page(folder_list[1]["filenames"])
    yield enter_nut_cloud_home


@pytest.fixture(scope="function")
def enter_folder_page(app_driver, enter_folder_page_parametrized, cleanup_manager):
    """参数化的进入文件夹页面fixture"""
    file_page = FilePage(enter_folder_page_parametrized.driver)
    file_page.register_cleanup = cleanup_manager.register_cleanup
    file_page.set_skip_default_cleanup = cleanup_manager.set_skip_default_cleanup
    # 进入文件夹
    
    yield file_page
    if not cleanup_manager.skip_default_cleanup:
        try:
            file_page.navigate_back(1)
        except Exception as e:
            logger.info(f"默认清理失败: {e}")


@pytest.fixture(scope="function")
def more_pop_window_page(app_driver, page_fixture, request: FixtureRequest, cleanup_manager):
    current_page = request.getfixturevalue(page_fixture)
    more_pop_window = current_page.MorePopWindow(app_driver)
    current_page.click_more_button()
    more_pop_window.register_cleanup = cleanup_manager.register_cleanup
    yield more_pop_window


@pytest.fixture(scope="function")
def bookshelf_home(app_switcher, app_driver, cleanup_manager):
    bookshelf_page = BookshelfPage(app_switcher.driver)
    bookshelf_page.register_cleanup = cleanup_manager.register_cleanup
    bookshelf_page.set_skip_default_cleanup = cleanup_manager.set_skip_default_cleanup
    yield bookshelf_page
