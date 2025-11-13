from collections import Counter

import allure
import pytest
from _pytest.fixtures import FixtureRequest


@pytest.mark.run(order=9)
@allure.story("搜索流程入口验证")
class TestSearchEntry:
    @pytest.mark.parametrize(
        "page_fixture, page_name",
        [
            ("enter_nut_cloud_home", "坚果云首页"),  # 第一个场景：首页
            ("enter_folder_page", "文件页面")  # 第二个场景：文件夹页面
        ]
    )
    @allure.title("用户验证是否进入搜索页面")
    def test_click_search_button(self, request: FixtureRequest, page_fixture, page_name):
        current_page = request.getfixturevalue(page_fixture)
        
        with allure.step("点击搜索按钮"):
            document_list = current_page.get_all_document_names()
            result = current_page.click_search_button()
            search_document_list = result.get_all_search_document_names()
        with allure.step("验证搜索框存在"):
            assert result.verify_enter_search_page() == '请输入搜索文件名', f"进入搜索页失败"
        with allure.step("验证搜索数据"):
            assert Counter(document_list) == Counter(search_document_list), f"点击搜索按钮后文件列表未正常显示"
    
    @allure.title("用户验证进入搜索页面点击返回")
    def test_return_home(self, enter_search_page):
        def click_search_but():
            enter_search_page.click_search_document_but()
        
        enter_search_page.register_cleanup(click_search_but)
        
        with allure.step("在搜素页点击返回按钮"):
            enter_search_page.click_search_return()
        with allure.step("验证回到网盘首页"):
            enter_search_page.verify_search_button_return_success(), f"搜索页面点击返回按钮返回失败"
