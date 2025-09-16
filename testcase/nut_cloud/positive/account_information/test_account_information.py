import logging

import allure
import pytest

from pages.nut_cloud_page.nut_login_page import NutLoginPage
from utils.test_data_loader import load_test_data

logger = logging.getLogger(__name__)
test_positive_data = load_test_data("positive_rename.json")
username = 'liuxuefeng@hanwang.com.cn'


@pytest.mark.run(order=3)
@allure.epic("长按坚果云网盘点击账户信息")
@allure.feature("账户信息模块")
class TestAccountInformationScenarios:
    
    @allure.story("用户输入名称")
    @allure.title("验证用户是否可以正常输入")
    @pytest.mark.parametrize("rename_data", test_positive_data,
                             ids=[item['description'] for item in test_positive_data])
    def test_input_account_name(self, logged_in_account_edit_page, rename_data):
        try:
            with allure.step("输入名称"):
                result = logged_in_account_edit_page.input_account(
                    rename_data['new_name']
                )
            assert result.verify_input_account_name() == rename_data['new_name'], f"账户名称输入失败"
        finally:
            result._safe_navigate_back(3)
    
    @allure.story("用户命名时点击取消")
    @allure.title("验证用户是否可以取消命名")
    def test_click_account_cancel_button(self, logged_in_account_edit_page):
        try:
            with allure.step("点击取消"):
                result = logged_in_account_edit_page.click_cancel_button()
                assert result.verify_return_account_information(), f"账户名称清除失败"
        finally:
            result._safe_navigate_back(1)
    
    @allure.story("用户命名时点击确定")
    @allure.title("验证用户是否可以确定命名")
    def test_click_account_sure_button(self, logged_in_account_edit_page):
        try:
            with allure.step("点击确定"):
                result = logged_in_account_edit_page.click_sure_button()
                assert result.verify_return_account_information(), f"账户名称编辑失败"
        finally:
            result._safe_navigate_back(1)
    
    @allure.story("用户输入名称后清除账户名称")
    @allure.title("验证用户是否可以正常输入后清除账户名称")
    @pytest.mark.parametrize("rename_data", test_positive_data,
                             ids=[item['description'] for item in test_positive_data])
    def test_input_account_name_delete(self, logged_in_account_edit_page, rename_data):
        try:
            with allure.step("输入名称"):
                result = logged_in_account_edit_page.input_account(
                    rename_data['new_name']
                )
            assert result.verify_input_account_name() == rename_data['new_name'], f"账户名称输入失败"
            with allure.step("清除账户名称"):
                result.click_delete_button()
            assert result.verify_input_account_name() == '', f"账户名称清除失败"
        finally:
            result._safe_navigate_back(3)
    
    @allure.story("用户输入名称点击确定")
    @allure.title("验证用户是否可以正常输入后确定")
    @pytest.mark.parametrize("rename_data", test_positive_data,
                             ids=[item['description'] for item in test_positive_data])
    def test_input_account_name(self, logged_in_account_edit_page, rename_data):
        logged_in_account_edit_page.set_skip_default_cleanup()
        
        def update_account_name():
            logged_in_account_edit_page.input_account(
                username
            ).click_sure_button()
        
        logged_in_account_edit_page.register_cleanup(update_account_name)
        try:
            with allure.step("输入名称"):
                result = logged_in_account_edit_page.input_account(
                    rename_data['new_name']
                )
            assert result.verify_input_account_name() == rename_data['new_name'], f"账户名称输入失败"
            with allure.step("点击确定"):
                result.click_sure_button()
            with allure.step("点击编辑按钮"):
                result.click_edit_button()
            assert result.verify_input_account_name() == rename_data['new_name'], f"账户名称输入失败"
        finally:
            result._safe_navigate_back(3)
    
    @allure.story("用户命名时点击回退名称")
    @allure.title("验证用户是否可以清除名称")
    def test_click_delete_button(self, logged_in_account_edit_page):
        try:
            
            with allure.step("点击回退"):
                result = logged_in_account_edit_page.click_delete_button()
                assert result.verify_input_account_name() == '', f"清除账户信息失败"
        finally:
            result._safe_navigate_back(3)
    
    @allure.story("用户点击账户信息按钮")
    @allure.title("验证是否进入账户信息界面")
    def test_click_return_button(self, logged_in_account_information_page):
        with allure.step("点击返回按钮"):
            result = logged_in_account_information_page.click_return_button()
            assert result.verify_return_home_page(), f"返回到主页失败"
    
    @allure.story("用户点击名称编辑按钮")
    @allure.title("验证是否进入编辑按钮界面")
    def test_click_edit_button(self, logged_in_account_information_page):
        with allure.step("点击编辑"):
            try:
                result = logged_in_account_information_page.click_edit_button()
                assert result.get_account_rename_text() == '重命名', f"点击编辑按钮失败"
            finally:
                result._safe_navigate_back(3)
    
    @allure.story("用户点击解绑按钮")
    @allure.title("验证是否出现解绑提示窗口")
    def test_click_unbind_button(self, logged_in_account_information_page):
        with allure.step("点击解绑"):
            try:
                result = logged_in_account_information_page.click_unbind_button()
                assert result.get_unbind_window_text() == '是否解绑？', f"点击解绑按钮失败"
            finally:
                result._safe_navigate_back(2)
    
    @allure.story("用户点击解绑按钮后点击取消")
    @allure.title("验证是否返回到账户信息页")
    def test_click_unbind_cancel_button(self, logged_in_account_information_page):
        try:
            with allure.step("点击解绑"):
                result = logged_in_account_information_page.click_unbind_button()
                assert result.get_unbind_window_text() == '是否解绑？', f"点击解绑按钮失败"
            with allure.step("点击取消"):
                result.click_unbind_cancel_button()
                assert result.verify_return_account(), f"点击取消按钮失败"
        finally:
            result._safe_navigate_back(1)
    
    @allure.story("用户点击解绑按钮后点击确定")
    @allure.title("验证是否返回到坚果云绑定页面")
    def test_click_unbind_sure_button(self, logged_in_account_information_page):
        logged_in_account_information_page.set_skip_default_cleanup()
        
        def bind_nut_cloud():
            nut_login_page = NutLoginPage(logged_in_account_information_page.driver)
            nut_login_page.login_successful()
        
        logged_in_account_information_page.register_cleanup(bind_nut_cloud)
        with allure.step("点击解绑"):
            result = logged_in_account_information_page.click_unbind_button()
            assert result.get_unbind_window_text() == '是否解绑？', f"点击解绑按钮失败"
        with allure.step("点击确定"):
            result.click_unbind_sure_button()
            assert result.verify_unbind_success(), f"点击取消按钮失败"
