import logging

import allure
import pytest

from utils.test_data_loader import load_test_data

logger = logging.getLogger(__name__)
login_data_positive = load_test_data("login_data_positive.json")
test_username = 'liuxuefeng@hanwang.com.cn'
test_password = 'ani2k9vrmac7epjp'


@allure.epic("坚果云网盘登陆页面测试")
@allure.feature("登录模块")
class TestLoginScenarios:
    @pytest.fixture
    def rename_data(self, request):
        return request.param
    
    def pytest_generate_tests(self, metafunc):
        # 检查当前测试函数是否在当前类中
        if metafunc.cls == self.__class__ and "login_data" in metafunc.fixturenames:
            # 为当前类中的测试函数统一参数化
            metafunc.parametrize("login_data", login_data_positive,
                                 ids=[item['description'] for item in login_data_positive])
    
    @allure.story("用户输入用户名")
    @allure.title("验证输入不同长度、字符用户名")
    def test_input_username(self, nut_cloud_login_page, login_data):
        with allure.step(f"账号输入: {login_data['username']}"):
            nut_cloud_login_page \
                .input_username(login_data['username']) \
                .assert_input_username(login_data['username'])
    
    @allure.story("用户输入密码-掩码")
    @allure.title("验证输入不同长度、字符密码")
    def test_input_password(self, nut_cloud_login_page, login_data):
        with allure.step(f"密码输入:{login_data['password']}"):
            nut_cloud_login_page \
                .input_password(login_data['password']) \
                .assert_password_hidden()
    
    @allure.story("用户点击返回按钮")
    @allure.title("验证点击返回按钮返回到绑定网盘主页")
    def test_click_return_button(self, nut_cloud_login_page):
        with allure.step("点击返回"):
            nut_cloud_login_page \
                .click_return_button() \
                .assert_click_return_button_home()
    
    @allure.story("用户点击显示密码按钮")
    @allure.title("验证用户点击显示密码按钮后文本是否正常显示为明码")
    def test_click_display_button(self, nut_cloud_login_page):
        nut_cloud_login_page \
            .click_password_display_button() \
            .assert_password_visible()
    
    @allure.story("用户取消登录")
    @allure.title("验证在登陆页面可点击取消")
    def test_click_cancel_button(self, nut_cloud_login_page, setup):
        with allure.step("取消登录"):
            nut_cloud_login_page \
                .click_cancel_button()
        with allure.step("重新进入网盘"):
            setup.click_nut_cloud_login_successful()
    
    @allure.story("用户点击确定")
    @allure.title("验证点击确定是否弹出对应提示")
    def test_click_sure_button(self, nut_cloud_login_page):
        with allure.step("确定登录"):
            nut_cloud_login_page \
                .click_sure() \
                .assert_toast_nut()
    
    @allure.story("用户输入用户名点击返回")
    @allure.title("验证输入用户名后点击返回是否回到主页")
    def test_input_username_return_workflow(self, nut_cloud_login_page, setup):
        with allure.step(f"输入账号，点击返回"):
            nut_cloud_login_page \
                .input_username(test_username) \
                .assert_input_username(test_username) \
                .click_return_button() \
                .assert_click_return_button_home()
        with allure.step("重新进入网盘"):
            setup.click_nut_cloud_login_successful()
    
    @allure.story("用户输入密码点击返回")
    @allure.title("验证输入密码后点击返回是否回到主页")
    def test_input_password_return_workflow(self, nut_cloud_login_page, setup):
        with allure.step(f"输入密码，点击返回"):
            nut_cloud_login_page \
                .input_username(test_password) \
                .assert_input_username(test_password) \
                .click_return_button() \
                .assert_click_return_button_home()
        with allure.step("重新进入网盘"):
            setup.click_nut_cloud_login_successful()
    
    @allure.story("用户输入账号，密码")
    @allure.title("验证用户输入账号后输入密码")
    def test_input_username_password_workflow(self, nut_cloud_login_page):
        with allure.step("输入账号，输入密码"):
            nut_cloud_login_page \
                .input_username(test_username) \
                .assert_input_username(test_username) \
                .input_password(test_password) \
                .assert_password_hidden()
    
    @allure.story("用户输入账号密码后点击取消登录")
    @allure.title("验证用户输入账号，输入密码，点击取消")
    def test_input_username_password_cancel_workflow(self, nut_cloud_login_page):
        with allure.step("输入账号，输入密码"):
            nut_cloud_login_page \
                .input_username(test_username) \
                .assert_input_username(test_username) \
                .input_password(test_password) \
                .assert_password_hidden() \
                .click_cancel_button()
    
    @allure.story("用户输入密码后查看密码")
    @allure.story("验证用户输入密码后查看明码")
    def test_input_password_click_display_workflow(self, nut_cloud_login_page):
        with allure.step("输入密码查看密码"):
            nut_cloud_login_page \
                .input_password(test_password) \
                .assert_password_hidden() \
                .click_password_display_button() \
                .assert_password_visible(test_password)
    
    @allure.story("用户输入密码显示明码再将密码恢复为掩码")
    @allure.title("验证密码明码变为掩码")
    def test_password_state_change_workflow(self, nut_cloud_login_page):
        with allure.step("密码明码变为掩码"):
            nut_cloud_login_page \
                .input_password(test_password) \
                .assert_password_hidden() \
                .click_password_display_button() \
                .assert_password_visible(test_password) \
                .click_password_display_button() \
                .assert_password_hidden()
    
    @allure.step("用户输入正确的账号密码进行登录")
    @allure.title("验证正确用户名密码登陆成功")
    def test_input_username_password_login_success(self, nut_cloud_login_page, login_data):
        with allure.step("正确登录"):
            nut_cloud_login_page \
                .input_username(login_data['username']) \
                .assert_input_username(login_data['username']) \
                .input_password(login_data['password']) \
                .assert_password_hidden() \
                .click_sure() \
                .verify_success_login()
