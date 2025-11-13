import logging

import allure
import pytest

logger = logging.getLogger(__name__)


@pytest.mark.run(order=6)
@allure.epic("网盘主页长按坚果云网盘")
@allure.feature("详情页模块")
class TestDetailsScenarios:
    @allure.story("用户点击关闭按钮")
    @allure.title("验证点击关闭按钮后是否返回到网盘主页")
    def test_details_click_close_button(self, logged_in_details_page):
        with allure.step("点击关闭按钮"):
            result = logged_in_details_page.click_close_button()
            assert result.verify_return_home(), f"返回主页失败"
    
    def test_details_click_account_button(self, logged_in_details_page):
        with allure.step("点击账户信息按钮"):
            try:
                result = logged_in_details_page.click_account_button()
                assert result.get_account_unbind_text() == '解绑', f"进入账户信息界面失败"
            finally:
                result.back()
    
    def test_details_click_rename_button(self, logged_in_details_page):
        with allure.step("点击重命名按钮"):
            try:
                result = logged_in_details_page.click_rename_button()
                assert result.get_rename_window_text() == '重命名', f"进入重命名界面失败"
            finally:
                result.navigate_back(2)
