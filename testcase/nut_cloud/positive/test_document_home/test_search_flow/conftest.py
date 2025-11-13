import logging

import pytest

from pages.nut_cloud_page.document_home_page import DocumentHomePage
from pages.nut_cloud_page.search_page import SearchPage

logger = logging.getLogger(__name__)


@pytest.fixture(scope="package")
def enter_search_flow(app_driver, enter_folder_page_parametrized):
    document_home_page = DocumentHomePage(app_driver)
    search_page = SearchPage(document_home_page.driver)
    document_home_page.click_search_button()
    yield search_page


@pytest.fixture(scope="function")
def enter_search_page(app_driver, enter_search_flow, cleanup_manager):
    """进入搜索页面"""
    enter_search_flow.register_cleanup = cleanup_manager.register_cleanup
    enter_search_flow.set_skip_default_cleanup = cleanup_manager.set_skip_default_cleanup
    yield enter_search_flow


@pytest.fixture(scope="function")
def input_name(request):
    """作为input_name参数的统一提供者，支持参数化传递"""
    return request.param  # 接收外部参数化传递的值


@pytest.fixture(scope="function")
def input_search_name(app_driver, enter_search_page, cleanup_manager, input_name):
    search_page = SearchPage(enter_search_page.driver)
    search_page.input_search_name(input_name)
    search_page.register_cleanup = cleanup_manager.register_cleanup
    search_page.set_skip_default_cleanup = cleanup_manager.set_skip_default_cleanup
    yield search_page


@pytest.fixture(scope="function")
def click_search_but(input_search_name, cleanup_manager):
    input_search_name.click_search_button()
    input_search_name.register_cleanup = cleanup_manager.register_cleanup
    input_search_name.set_skip_default_cleanup = cleanup_manager.set_skip_default_cleanup
    yield input_search_name


@pytest.fixture(scope="function")
def click_file_checkbox(click_search_but, input_name, check_test_data, cleanup_manager):
    """点击勾选"""
    click_search_but.click_search_file_name(check_test_data)
    input_search_name.register_cleanup = cleanup_manager.register_cleanup
    input_search_name.set_skip_default_cleanup = cleanup_manager.set_skip_default_cleanup
    yield click_search_but
