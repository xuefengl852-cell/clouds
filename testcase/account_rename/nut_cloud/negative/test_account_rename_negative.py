import logging

import allure
import pytest

from utils.test_data_loader import load_test_data

test_negative_data = load_test_data("negative_rename.json")

logger = logging.getLogger(__name__)


@allure.epic("重命名逆向模块")  # 使用更规范的层级标签
@allure.feature("账户重命名功能")
class TestAccountRenameNegative:
    
    @pytest.fixture
    def rename_data(self, request):
        return request.param
    
    def pytest_generate_tests(self, metafunc):
        # 检查当前测试函数是否在当前类中
        if metafunc.cls == self.__class__ and "rename_data" in metafunc.fixturenames:
            # 为当前类中的测试函数统一参数化
            metafunc.parametrize("rename_data", test_negative_data,
                                 ids=[item['description'] for item in test_negative_data])
    
    @pytest.mark.positive
    def test_input_account_name_negative(self, logged_in_account_rename_page, rename_data):
        allure.dynamic.title(rename_data['description'])
        with allure.step("网盘重命名-空值"):
            logged_in_account_rename_page \
                .input_account_name(rename_data['new_name']) \
                .assert_input_text(rename_data['new_name'])
    
    @allure.story("输入后点击确定-空值")
    def test_input_cancel__negative_workflow(self, logged_in_account_rename_page, rename_data):
        with allure.step("输入名称后点击确定按钮"):
            logged_in_account_rename_page \
                .input_account_name(rename_data['new_name']) \
                .assert_input_text(rename_data['new_name']) \
                .click_sure_button() \
                .assert_rename_success_toast(rename_data['expected_error'])
