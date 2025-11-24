import logging

import pytest

from pages.nut_cloud_page.document_home_page import DocumentHomePage

logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")  # 明确指定function级别（默认也是function，可省略）
def checked_interface_with_cleanup(enter_search_page, check_test_data, cleanup_manager):
    """
    依赖keep_checked_interface，保持勾选界面状态，并在测试后执行清理动作
    """
    interface = enter_search_page
    document_home_page = DocumentHomePage(enter_search_page.driver)
    interface.click_search_file_name(check_test_data)
    interface.register_cleanup = cleanup_manager.register_cleanup
    interface.set_skip_default_cleanup = cleanup_manager.set_skip_default_cleanup
    yield interface  # 传递界面操作对象给测试用例.click_search_file_name(check_test_data)
    if not cleanup_manager.skip_default_cleanup:
        try:
            interface.navigate_back(1)
            document_home_page.click_search_button()
        except Exception as e:
            logger.info(f"默认清理失败: {e}")


@pytest.fixture(scope="function")  # 明确指定function级别（默认也是function，可省略）
def click_select_all_but(checked_interface_with_cleanup, check_test_data, cleanup_manager):
    checked_interface_with_cleanup.set_skip_default_cleanup()
    result = checked_interface_with_cleanup
    result.click_select_all_but()
    result.register_cleanup = cleanup_manager.register_cleanup
    result.set_skip_default_cleanup = cleanup_manager.set_skip_default_cleanup
    yield result  # 传递界面操作对象给测试用例.click_search_file_name(check_test_data)
