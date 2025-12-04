import pytest

from pages.nut_cloud_page.document_home_page import DocumentHomePage
from pages.nut_cloud_page.search_copy_page import SearchCopyPage
from pages.nut_cloud_page.search_page import SearchPage


@pytest.fixture(scope="package")
def search_base_state(app_driver, app_info, enter_folder_page_parametrized):
    """package 级：仅初始化页面实例，不执行业务操作，保证无参数依赖"""
    # 步骤1：打开搜索页面（整个包只执行1次，基础状态）
    document_home_page = DocumentHomePage(app_driver, app_info)
    search_page = SearchPage(document_home_page.driver)
    document_home_page.click_search_button()
    
    # 步骤2：初始化复制页面实例（复用驱动，不打开窗口）
    copy_page = SearchCopyPage(search_page.driver)
    
    # 状态管理：标记「是否已完成「勾选→复制」完整流程」
    # 用字典存储，避免 mutable 变量的作用域污染
    flow_state = {
        "is_checked": False,  # 是否已勾选文件
        "is_copied": False,  # 是否已执行复制
        "is_enter_folder_first": False,  # 是否进入第一层文件夹
        "is_enter_folder_second": False  # 是否进入第二层文件夹
    }
    
    yield search_page, copy_page, flow_state  # 提供核心实例+状态标记


@pytest.fixture(scope="function")
def folder_name_first(request):
    return request.param  # 接收外部参数化传递的值


@pytest.fixture(scope="function")
def enter_folder_second(request):
    return request.param  # 接收外部参数化传递的值


@pytest.fixture(scope="function")
def click_search_copy_btn(search_base_state, check_test_data, folder_name_first, enter_folder_second, cleanup_manager):
    """function 级：严格保证「勾选→复制」顺序，仅首次执行完整流程"""
    search_page, copy_page, flow_state = search_base_state
    
    # 核心逻辑：仅首次执行「勾选→复制」，且严格保证顺序
    if not flow_state["is_copied"]:  # 未执行复制时才触发
        # 步骤1：勾选文件（用动态参数，必须成功后才继续）
        target_file = check_test_data
        search_page.click_search_file_name(target_file)
        flow_state["is_checked"] = True  # 更新勾选状态
        search_page.click_copy_btn()
        flow_state["is_copied"] = True  # 更新复制状态
        copy_page.enter_copy_page_folder_name(folder_name_first)
        flow_state["is_enter_folder_first"] = True  # 更新进入第一次文件夹状态
        copy_page.enter_copy_page_folder_name(enter_folder_second)
        flow_state["is_enter_folder_second"] = True  # 更新进入第二次文件夹状态
    # 注册局部清理（不影响全局状态，如重置复制窗口状态）
    copy_page.register_cleanup = cleanup_manager.register_cleanup
    copy_page.set_skip_default_cleanup = cleanup_manager.set_skip_default_cleanup
    
    yield copy_page


@pytest.fixture(scope="function")
def click_search_copy_new_folder_btn(click_search_copy_btn, check_test_data, cleanup_manager):
    """点击搜索页-复制-新建文件夹按钮"""
    click_search_copy_btn.click_new_folder()
    click_search_copy_btn.register_cleanup = cleanup_manager.register_cleanup
    click_search_copy_btn.set_skip_default_cleanup = cleanup_manager.set_skip_default_cleanup
    yield click_search_copy_btn
