import logging

import allure
import pytest

logger = logging.getLogger(__name__)


@pytest.mark.login_required
@allure.feature("账户信息模块")
class TestAccountInformationScenarios:
    
    def test_click_return_button(self, logged_in_account_information_page):
        with allure.step("点击返回按钮"):
            logged_in_account_information_page.click_return_button()
        with allure.step("验证返回按钮"):
            logged_in_account_information_page.assert_click_return_button()
    
    def test_click_edit_button(self, logged_in_account_information_page):
        with allure.step("点击编辑按钮"):
            logged_in_account_information_page.click_edit_button()
        with allure.step("验证返回按钮"):
            logged_in_account_information_page.assert_click_edit_button()
    
    def test_click_unbind_button(self, logged_in_account_information_page):
        with allure.step("点击解绑按钮"):
            logged_in_account_information_page.click_unbind_button()
        with allure.step("验证解绑按钮"):
            logged_in_account_information_page.assert_click_unbind_button()
