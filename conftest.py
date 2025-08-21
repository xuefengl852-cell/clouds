import base64
import logging
import os
import subprocess
from datetime import datetime
from io import BytesIO
from logging.handlers import TimedRotatingFileHandler

import allure
import pytest
from PIL import Image
from appium import webdriver
from loguru import logger

from pages.home_clouds_page import HomeCloudsPage
from pages.nut_cloud_page.home_page import HomePage
from pages.nut_cloud_page.nut_login_page import NutLoginPage
# 从配置模块导入
from utils.driver import init_driver

# 获取项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 全局配置
SCREENSHOT_DIR = os.path.join(BASE_DIR, "reports", "screenshots")
VIDEO_DIR = os.path.join(BASE_DIR, "reports", "videos")
ALLURE_RESULTS_DIR = os.path.join(BASE_DIR, "allure-results")
MAX_RECORDINGS = 20  # 最大录制文件数

# 初始化日志
logger = logging.getLogger(__name__)


def custom_log_namer(default_name):
    """
    自定义日志文件命名格式
    将默认的 pytest.log.2025-08-05 改为 pytest_2025-08-05.log
    """
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
    # 确保日志目录存在
    log_dir = os.path.join(BASE_DIR, "logs")
    os.makedirs(log_dir, exist_ok=True)
    
    # 创建按天轮转的日志处理器
    log_file = os.path.join(log_dir, "pytest.log")  # 基础日志文件名
    
    # 创建 TimedRotatingFileHandler - 使用本地时间
    file_handler = TimedRotatingFileHandler(
        filename=log_file,
        when="midnight",  # 每天午夜轮转
        interval=1,  # 每天一次
        backupCount=30,  # 保留30天
        encoding="utf-8",
        utc=False  # 使用本地时间
    )
    # 应用自定义命名函数设置文件名格式（推荐）
    file_handler.namer = custom_log_namer  # 轮转文件后缀格式
    # 或者使用更精确的格式（可选）:
    # file_handler.suffix = "%Y-%m-%d_%H-%M-%S.log"
    
    # 设置日志格式
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-8s | %(name)s:%(lineno)d | %(message)s",
        "%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)
    
    # 配置根日志记录器
    root_logger = logging.getLogger()
    root_logger.addHandler(file_handler)
    root_logger.setLevel(logging.DEBUG)
    # 创建所有需要的目录
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    os.makedirs(VIDEO_DIR, exist_ok=True)
    os.makedirs(ALLURE_RESULTS_DIR, exist_ok=True)
    
    # 设置 Allure 结果目录
    config.option.allure_report_dir = ALLURE_RESULTS_DIR
    
    # 清理旧截图和录制文件
    cleanup_old_files(SCREENSHOT_DIR, ['.png'], MAX_RECORDINGS)
    cleanup_old_files(VIDEO_DIR, ['.mp4'], MAX_RECORDINGS)
    
    # # 记录路径信息
    # logger.info("=" * 50)
    # logger.info(f"项目根目录: {BASE_DIR}")
    # logger.info(f"截图目录: {SCREENSHOT_DIR}")
    # logger.info(f"视频目录: {VIDEO_DIR}")
    # logger.info(f"Allure 结果目录: {ALLURE_RESULTS_DIR}")
    # logger.info("=" * 50)


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


def cleanup_old_files(directory, extensions, max_files):
    """清理旧文件，保留最新的 max_files 个指定扩展名的文件"""
    if not os.path.exists(directory):
        return
    
    try:
        # 获取所有指定扩展名的文件并按修改时间排序
        files = []
        for f in os.listdir(directory):
            if any(f.lower().endswith(ext) for ext in extensions):
                files.append(os.path.join(directory, f))
        
        files = sorted(
            files,
            key=os.path.getmtime,
            reverse=True
        )
        
        # 删除超出保留数量的旧文件
        for old_file in files[max_files:]:
            try:
                os.remove(old_file)
                logger.info(f"已删除旧文件: {os.path.basename(old_file)}")
            except Exception as e:
                logger.warning(f"删除文件失败: {e}", exc_info=True)
    
    except Exception as e:
        logger.error(f"清理文件时发生错误: {e}", exc_info=True)


@pytest.fixture(scope="function", autouse=True)
def screen_recording(request):
    """测试用例屏幕录制功能"""
    # 从测试用例的fixture中查找driver实例
    driver = None
    for fixture_name in request.fixturenames:
        try:
            fixture_value = request.getfixturevalue(fixture_name)
            if isinstance(fixture_value, webdriver.Remote):
                driver = fixture_value
                break
        except Exception:
            continue
    
    if driver is None:
        logger.warning("未找到driver实例，跳过屏幕录制")
        yield
        return
        
        # 检查driver是否支持屏幕录制
    if not hasattr(driver, 'start_recording_screen'):
        logger.warning("当前驱动不支持屏幕录制功能")
        yield
        return
        
        # 生成安全的录制文件名 - 处理Unicode字符问题
    test_name = request.node.name
    safe_test_name = "".join(
        c if c.isalnum() or c in ('_', '-') else '_'
        for c in test_name
    )[:50]  # 限制文件名长度
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    video_filename = f"VIDEO_{safe_test_name}_{timestamp}.mp4"
    video_path = os.path.join(VIDEO_DIR, video_filename)
    
    # 确保目录存在（再次检查）
    os.makedirs(os.path.dirname(video_path), exist_ok=True)
    
    # 开始录制
    try:
        # 设置录制参数
        video_options = {
            "timeLimit": 300,  # 5分钟限制
            "bitRate": 4000000,  # 4 Mbps
            "videoSize": "1280x720"  # Android特有参数
        }
        
        driver.start_recording_screen(**video_options)
        logger.info(f"开始屏幕录制: {video_path}")
    except Exception as e:
        logger.error(f"启动屏幕录制失败: {e}", exc_info=True)
        yield
        return
    
    # 将视频路径附加到测试节点
    request.node.video_path = video_path
    
    yield
    
    # 停止录制并保存视频
    try:
        video_data = driver.stop_recording_screen()
        logger.info(f"停止屏幕录制: {video_path}")
        
        # 保存录制的视频
        with open(video_path, "wb") as f:
            f.write(base64.b64decode(video_data))
        
        logger.info(f"屏幕录制已保存: {video_path}")
    except Exception as e:
        logger.error(f"保存屏幕录制失败: {e}", exc_info=True)
        
        # 尝试保存错误信息
        try:
            error_log_path = os.path.join(VIDEO_DIR, f"ERROR_{safe_test_name}_{timestamp}.log")
            with open(error_log_path, "w") as f:
                f.write(f"录制保存失败: {str(e)}\n")
                f.write(f"测试名称: {test_name}\n")
                f.write(f"视频路径: {video_path}\n")
        except Exception as log_error:
            logger.error(f"保存错误日志失败: {log_error}")


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


@pytest.fixture(scope="session")
def app_driver(request):
    # 获取命令行参数
    device_id = request.config.getoption("--device-id", default=None)
    app_package = request.config.getoption("--app-package", default="com.example.app")
    app_activity = request.config.getoption("--app-activity", default=".MainActivity")
    
    # 执行智能清理
    clean_database(device_id)
    """创建并返回Appium driver"""
    driver = init_driver()
    yield driver
    driver.quit()


@pytest.fixture(scope="session")
def setup(app_driver):  # 注意：这里移除了self参数
    home_cloud_page = HomeCloudsPage(app_driver)
    yield home_cloud_page


@pytest.fixture(scope="session")
def nut_cloud_logged(app_driver, setup):
    setup.click_nut_cloud_success()
    yield app_driver


@pytest.fixture(scope="session")
def logged_in_driver(nut_cloud_logged, app_driver):
    """Session 范围的已登录 driver"""
    login_page = NutLoginPage(app_driver)
    home_page = login_page.login_successful()
    yield app_driver


@pytest.fixture(scope="function")
def nut_cloud_login_page(logged_in_driver, app_driver):
    home_page = HomePage(app_driver)
    yield home_page
    home_page.back()


# 获取有效的登录凭证
@pytest.fixture(scope="session")
def logged_in_home_page(logged_in_driver, app_driver):
    home_page = HomePage(app_driver)
    yield home_page
    home_page.back()


# 获取绑定网盘窗口页
@pytest.fixture(scope="function")
def logged_in_details_page(logged_in_home_page):
    yield logged_in_home_page.long_press_cloud_fixture()


@pytest.fixture(scope="function")
def cloud_more_window(logged_in_home_page):
    more_window = logged_in_home_page.click_more_button_workflow()
    yield more_window
    more_window


# 获取账户信息页
@pytest.fixture(scope="function")
def logged_in_account_information_page(logged_in_details_page):
    try:
        # 使用新的导航方法
        account_info_page = logged_in_details_page.navigate_to_account_information()
        return account_info_page
    except Exception as e:
        logger.error(f"账户信息页加载失败: {str(e)}")
        logged_in_details_page.driver.save_screenshot("account_info_page_load_failure.png")
        pytest.fail(f"无法加载账户信息页: {str(e)}")


# 获取重命名页
@pytest.fixture(scope="function")
def logged_in_account_rename_page(logged_in_details_page, logged_in_home_page):
    try:
        # 使用新的导航方法
        account_info_page = logged_in_details_page.navigate_to_account_rename()
        yield account_info_page
        account_info_page
        logged_in_home_page.long_press_cloud()
    except Exception as e:
        logger.error(f"账户信息页加载失败: {str(e)}")
        pytest.fail(f"无法加载账户信息页: {str(e)}")


# 获取重命名页
@pytest.fixture(scope="function")
def logged_in_account_rename_page(logged_in_details_page):
    try:
        # 使用新的导航方法
        account_info_page = logged_in_details_page.navigate_to_account_rename()
        yield account_info_page
    except Exception as e:
        logger.error(f"账户信息页加载失败: {str(e)}")
        pytest.fail(f"无法加载账户信息页: {str(e)}")
