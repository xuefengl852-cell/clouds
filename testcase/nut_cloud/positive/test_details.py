import logging

import allure
import pytest

logger = logging.getLogger(__name__)


@pytest.mark.login_required
@allure.feature("主页登录模块")
class TestDetailsScenarios:
    @pytest.mark.smoke  # 👈 标记为冒烟测试
    def test_details_click_close_button(self, logged_in_details_page):
        with allure.step("点击关闭按钮"):
            logged_in_details_page.click_close_button()
        with allure.step("验证关闭按钮"):
            logged_in_details_page.assert_click_close_button()
    
    def test_details_click_account_button(self, logged_in_details_page):
        with allure.step("点击账户信息按钮"):
            logged_in_details_page.click_account_button()
        with allure.step("验证账户信息按钮"):
            logged_in_details_page.assert_click_account_button()
    
    def test_details_click_rename_button(self, logged_in_details_page):
        with allure.step("点击重命名按钮"):
            logged_in_details_page.click_rename_button()
        with allure.step("验证重命名按钮"):
            logged_in_details_page.assert_click_rename_button()
