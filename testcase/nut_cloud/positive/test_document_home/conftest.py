import pytest

from pages.nut_cloud_page.document_home_page import DocumentHomePage
from utils.test_data_loader import load_test_data

list_pattern_coordinates_data = load_test_data("list_pattern_coordinates.json")


@pytest.fixture(scope="function")
def click_list_pattern(app_driver):
    more_pop_window = DocumentHomePage.MorePopWindow(app_driver)
    more_pop_window.click_specify_coordinates(list_pattern_coordinates_data)
    yield more_pop_window


@pytest.fixture(scope="function")
def click_more_button(app_driver, enter_folder_page_parametrized):
    # 根据 page_fixture 获取对应的页面实例
    # 执行点击更多按钮操作
    enter_folder_page_parametrized.click_more_button()
    yield enter_folder_page_parametrized


@pytest.fixture(scope="function")
def page_swipe_down(app_driver, enter_nut_cloud_home):
    enter_nut_cloud_home.page_swipe_left_down(down=True)
    yield enter_nut_cloud_home
