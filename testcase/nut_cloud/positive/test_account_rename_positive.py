import logging

import allure
import pytest

from utils.test_data_loader import load_test_data

test_positive_data = load_test_data("positive_rename.json")
logger = logging.getLogger(__name__)
new_name = "网盘重命名名称测试"
default_placeholder = "输入网盘名称"
success_toast = "重命名成功"


@pytest.mark.login_required
@allure.epic("账户模块")  # 使用更规范的层级标签
@allure.feature("账户重命名正向用例模块")
class TestAccountRenamePositive:
    
    @pytest.fixture
    def rename_data(self, request):
        return request.param
    
    def pytest_generate_tests(self, metafunc):
        # 检查当前测试函数是否在当前类中
        if metafunc.cls == self.__class__ and "rename_data" in metafunc.fixturenames:
            # 为当前类中的测试函数统一参数化
            metafunc.parametrize("rename_data", test_positive_data,
                                 ids=[item['description'] for item in test_positive_data])
    
    @pytest.mark.positive
    def test_input_account_name(self, logged_in_account_rename_page, rename_data):
        allure.dynamic.title(rename_data['description'])
        with allure.step("网盘重命名"):
            logged_in_account_rename_page \
                .input_account_name(rename_data['new_name']) \
                .assert_input_text(rename_data['new_name']) \
                .click_press_back_button() \
                .click_press_back_button() \
                .assert_return_home()
    
    @allure.story("名称回退功能")
    @pytest.mark.positive
    def test_click_delete_name(self, logged_in_account_rename_page):
        with allure.step("点击回退按钮"):
            logged_in_account_rename_page \
                .click_delete_name() \
                .assert_input_text(default_placeholder)
    
    @allure.story("确认功能")
    @pytest.mark.positive
    def test_click_sure_button(self, logged_in_account_rename_page):
        with allure.step("点击确定按钮"):
            logged_in_account_rename_page \
                .click_sure_button() \
                .assert_rename_success_toast(success_toast)
    
    def test_click_cancel_button(self, logged_in_account_rename_page):
        with allure.step("点击取消按钮"):
            logged_in_account_rename_page \
                .click_cancel_button() \
                .assert_return_home()
    
    @allure.story("输入后回退")
    def test_input_delete_workflow(self, logged_in_account_rename_page):
        with allure.step("输入名称后点击回退"):
            logged_in_account_rename_page \
                .input_account_name(new_name) \
                .assert_input_text(new_name) \
                .click_delete_name() \
                .assert_input_text(default_placeholder)
    
    @allure.story("输入后点击确定")
    def test_input_cancel_workflow(self, logged_in_account_rename_page, rename_data):
        with allure.step("输入名称后点击确定按钮"):
            logged_in_account_rename_page \
                .input_account_name(rename_data['new_name']) \
                .assert_input_text(rename_data['new_name']) \
                .click_sure_button() \
                .assert_rename_success_toast(rename_data['success_toast'])
    
    @allure.story("输入后点击取消")
    def test_input_cancel_workflow(self, logged_in_account_rename_page):
        with allure.step("输入名称后点击确定按钮"):
            logged_in_account_rename_page \
                .input_account_name(new_name) \
                .assert_input_text(new_name) \
                .click_cancel_button() \
                .assert_return_home()
    
    @allure.story("输入后回退点击取消")
    def test_input_delete_cancel_workflow(self, logged_in_account_rename_page):
        with allure.step("输入后回退点击取消"):
            logged_in_account_rename_page \
                .input_account_name(new_name) \
                .assert_input_text(new_name) \
                .click_delete_name() \
                .assert_input_text(default_placeholder) \
                .click_cancel_button() \
                .assert_return_home()
    
    @allure.story("输入回退输入确定")
    def test_input_delete_input_sure_workflow(self, logged_in_account_rename_page, rename_data):
        with allure.step("输入后回退再次输入点击确定"):
            logged_in_account_rename_page \
                .input_account_name(rename_data['new_name']) \
                .assert_input_text(rename_data['new_name']) \
                .click_delete_name() \
                .assert_input_text(rename_data['default_placeholder']) \
                .input_account_name(rename_data['new_name']) \
                .assert_input_text(rename_data['new_name']) \
                .click_sure_button() \
                .assert_rename_success_toast(rename_data['success_toast'])
