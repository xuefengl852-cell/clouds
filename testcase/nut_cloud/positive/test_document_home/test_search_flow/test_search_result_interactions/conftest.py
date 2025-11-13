import pytest

from utils.test_data_loader import load_test_data

check_data = load_test_data("search_results_check_data.json")


@pytest.fixture(scope="function")
def check_test_data(request):
    """接收测试数据参数的fixture，供enter_search_page等依赖使用"""
    return request.param  # 接收外部参数化传递的值


@pytest.fixture
def cancel_checkbox(click_search_but, check_test_data, cleanup_manager):
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
