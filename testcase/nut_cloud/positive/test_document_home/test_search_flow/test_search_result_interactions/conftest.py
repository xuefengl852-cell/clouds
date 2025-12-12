import logging

import pytest

from pages.nut_cloud_page.document_home_page import DocumentHomePage
from utils.test_data_loader import load_test_data

logger = logging.getLogger(__name__)
check_data = load_test_data("search_results_check_data.json")


@pytest.fixture(scope="function")
def check_test_data(request):
    """接收测试数据参数的fixture，供enter_search_page等依赖使用"""
    return request.param  # 接收外部参数化传递的值


@pytest.fixture
def cancel_checkbox(click_search_but, check_test_data, cleanup_manager):
    """根据搜索结果勾选文件"""
    click_search_but.click_search_file_name(check_test_data)
    click_search_but.register_cleanup = cleanup_manager.register_cleanup
    click_search_but.set_skip_default_cleanup = cleanup_manager.set_skip_default_cleanup
    yield click_search_but


@pytest.fixture(scope="function")
def long_file_data(request):
    return request.param


@pytest.fixture(scope="function")
def long_file_name(click_search_but, long_file_data, check_test_data, input_name, cleanup_manager):
    click_search_but.long_press_file_name(long_file_data)
    click_search_but.register_cleanup = cleanup_manager.register_cleanup
    click_search_but.set_skip_default_cleanup = cleanup_manager.set_skip_default_cleanup
    yield click_search_but


@pytest.fixture(scope="function")
def select_all_files(enter_search_page):
    """
    调用 get_select_all_text 方法，获取全选后的文件名称列表
    """
    search_page = enter_search_page
    file_names = search_page.get_select_all_text()  # 得到文件名称列表
    yield file_names


@pytest.fixture(scope="function")
def search_check_box_file(enter_search_flow, check_test_data, cleanup_manager):
    enter_search_flow.click_search_file_name(check_test_data)
    document_home_page = DocumentHomePage(enter_search_flow.driver)
    enter_search_flow.register_cleanup = cleanup_manager.register_cleanup
    enter_search_flow.set_skip_default_cleanup = cleanup_manager.set_skip_default_cleanup
    yield enter_search_flow, document_home_page
