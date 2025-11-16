import logging

import allure
import pytest

from utils.test_data_loader import load_test_data

test_positive_data = load_test_data("positive_rename.json")
logger = logging.getLogger(__name__)
new_name = "网盘重命名名称测试"
default_placeholder = "输入网盘名称"
success_toast = "重命名成功"


@pytest.mark.run(order=5)
@pytest.mark.login_required
@allure.epic("账户模块")  # 使用更规范的层级标签
@allure.feature("账户重命名正向用例模块")
class TestAccountRenamePositive:
    
    @pytest.mark.parametrize("rename_data", test_positive_data,
                             ids=[item['description'] for item in test_positive_data])
    @allure.story("用户输入不同长度名称")
    def test_input_account_name(self, logged_in_account_rename_page, rename_data):
        allure.dynamic.title(rename_data['description'])
        try:
            with allure.step("网盘重命名"):
                result = logged_in_account_rename_page.input_account_name(rename_data['new_name'])
                assert result.verify_input_text() == rename_data['new_name'], f"账户名称输入错误"
        finally:
            result._safe_navigate_back(2)
    
    @allure.story("用户点击清除名称按钮")
    @allure.title("验证将名称清除")
    def test_click_delete_name(self, logged_in_account_rename_page):
        try:
            with allure.step("点击回退"):
                result = logged_in_account_rename_page.click_delete_name()
                assert result.verify_input_text() == '输入网盘名称', f"账户清空失败"
        finally:
            result._safe_navigate_back(2)
    
    @allure.story("用户点击确认")
    @allure.title("验证提示重命名成功提示")
    def test_click_sure_button(self, logged_in_account_rename_page):
        with allure.step("点击确定按钮"):
            result = logged_in_account_rename_page.click_sure_button()
            assert result.verify_rename_success_toast('重命名成功')
    
    @allure.story("用户点击取消")
    @allure.title("验证返回到网盘首页")
    def test_click_cancel_button(self, logged_in_account_rename_page):
        with allure.step("点击取消按钮"):
            result = logged_in_account_rename_page.click_cancel_button()
            assert result.verify_return_home(), f"点击取消失败未回到首页"
    
    @pytest.mark.parametrize("rename_data", test_positive_data,
                             ids=[item['description'] for item in test_positive_data])
    @allure.story("用户输入不同长度名称后点击确定")
    def test_input_account_name_sure(self, logged_in_account_rename_page, rename_data):
        
        allure.dynamic.title(rename_data['description'])
        with allure.step("网盘重命名"):
            result = logged_in_account_rename_page.input_account_name(rename_data['new_name'])
            assert result.verify_input_text() == rename_data['new_name'], f"账户名称输入错误"
        with allure.step("点击确定按钮"):
            account_text = logged_in_account_rename_page.verify_input_account_name()
            result = logged_in_account_rename_page.click_sure_button()
            assert result.verify_home_cloud_name() == account_text, f"输入名称与首页名称不符"
            assert result.verify_rename_success_toast('重命名成功')
    
    @pytest.mark.parametrize("rename_data", test_positive_data,
                             ids=[item['description'] for item in test_positive_data])
    @allure.story("用户输入不同长度名称后点击清除点击确定")
    def test_input_account_name(self, logged_in_account_rename_page, rename_data):
        allure.dynamic.title(rename_data['description'])
        try:
            with allure.step("网盘重命名"):
                result = logged_in_account_rename_page.input_account_name(rename_data['new_name'])
                assert result.verify_input_text() == rename_data['new_name'], f"账户名称输入错误"
            with allure.step("点击回退"):
                result = logged_in_account_rename_page.click_delete_name()
                assert result.verify_input_text() == '输入网盘名称', f"账户清空失败"
            with allure.step("点击确定按钮"):
                result = logged_in_account_rename_page.click_sure_button()
                assert result.verify_rename_success_toast('请输入名称，名称不能为空')
        finally:
            result._safe_navigate_back(2)
