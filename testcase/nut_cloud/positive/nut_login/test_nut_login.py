import logging

import allure
import pytest

from pages.nut_cloud_page.account_information_page import AccountInformationPage
from pages.nut_cloud_page.details_page import DetailsPage
from pages.nut_cloud_page.home_page import HomePage
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
    def test_input_username(self, nut_cloud_login, login_data):
        with allure.step(f"账号输入: {login_data['username']}"):
            result = nut_cloud_login.input_username(login_data['username'])
            assert len(result.get_input_username_text()) == len(login_data['username']), f"断言账号长度相同失败"
            assert result.get_input_username_value() == login_data[
                'username'], f"断言失败，输入用户名与获取用户名值不相同"
    
    @allure.story("用户输入密码-掩码")
    @allure.title("验证输入不同长度、字符密码")
    def test_input_password(self, nut_cloud_login, login_data):
        with allure.step(f"密码输入:{login_data['password']}"):
            result = nut_cloud_login.input_password(login_data['password'])
            assert len(result.get_input_password_text()) == len(login_data['password']), f"断言密码长度相同失败"
            assert all(char in ['●', '*', '•'] for char in result.get_input_password_text()), "掩码字符不符合预期"
    
    @allure.story("用户点击返回按钮")
    @allure.title("验证点击返回按钮返回到绑定网盘主页")
    def test_click_return_button(self, nut_cloud_login):
        nut_cloud_login.set_skip_default_cleanup()
        with allure.step("点击返回"):
            result = nut_cloud_login.click_return_button()
            assert result.get_cloud_name_text() == '网盘', f"返回网盘主页失败"
    
    @allure.story("用户点击显示密码按钮")
    @allure.title("验证用户点击显示密码按钮后文本是否正常显示为明码")
    def test_click_display_button(self, nut_cloud_login, login_data):
        with allure.step("点击显示密码"):
            result = nut_cloud_login \
                .input_password(login_data['password']) \
                .click_password_display_button()
            assert result.get_input_password_text() == login_data['password'], f"密码显示按钮点击失败"
    
    @allure.story("用户取消登录")
    @allure.title("验证在登陆页面可点击取消")
    def test_click_cancel_button(self, nut_cloud_login):
        nut_cloud_login.set_skip_default_cleanup()
        with allure.step("取消登录"):
            result = nut_cloud_login.click_cancel_button()
            assert result.get_cloud_name_text() == '网盘', f"返回网盘主页失败"
    
    @allure.story("用户点击确定")
    @allure.title("验证点击确定是否弹出对应提示")
    def test_click_sure_button(self, nut_cloud_login):
        with allure.step("确定登录"):
            result = nut_cloud_login.click_sure()
            assert result.get_toast_page_text() == '请输入您的账号', f"点击确定失败"
    
    @allure.story("用户输入用户名点击返回")
    @allure.title("验证输入用户名后点击返回是否回到主页")
    def test_input_username_return_workflow(self, nut_cloud_login):
        nut_cloud_login.set_skip_default_cleanup()
        with allure.step(f"输入账号，点击返回"):
            result = nut_cloud_login.input_username(test_username)
            assert result.get_input_username_value() == test_username, f"断言失败，输入用户名与获取用户名值不相同"
            result.click_return_button()
            assert result.get_cloud_name_text() == '网盘', f"返回网盘主页失败"
    
    @allure.story("用户输入密码点击返回")
    @allure.title("验证输入密码后点击返回是否回到主页")
    def test_input_password_return_workflow(self, nut_cloud_login):
        nut_cloud_login.set_skip_default_cleanup()
        with allure.step(f"输入密码，点击返回"):
            result = nut_cloud_login.input_password(test_password)
            assert len(result.get_input_password_text()) == len(test_password), f"断言密码长度相同失败"
            assert all(char in ['●', '*', '•'] for char in result.get_input_password_text()), "掩码字符不符合预期"
            result.click_return_button()
            assert result.get_cloud_name_text() == '网盘', f"返回网盘主页失败"
    
    @allure.story("用户输入账号，密码")
    @allure.title("验证用户输入账号后输入密码")
    def test_input_username_password_workflow(self, nut_cloud_login):
        with allure.step("输入账号，输入密码"):
            result = nut_cloud_login.input_username(test_username)
            assert len(result.get_input_username_text()) == len(test_username), f"断言账号长度相同失败"
            assert result.get_input_username_value() == test_username, f"断言失败，输入用户名与获取用户名值不相同"
            result.input_password(test_password)
            assert len(result.get_input_password_text()) == len(test_password), f"断言密码长度相同失败"
            assert all(char in ['●', '*', '•'] for char in result.get_input_password_text()), "掩码字符不符合预期"
    
    @allure.story("用户输入账号密码后点击取消登录")
    @allure.title("验证用户输入账号，输入密码，点击取消")
    def test_input_username_password_cancel_workflow(self, nut_cloud_login):
        nut_cloud_login.set_skip_default_cleanup()
        with allure.step("输入账号，输入密码，点击取消"):
            result = nut_cloud_login.input_username(test_username)
            assert len(result.get_input_username_text()) == len(test_username), f"断言账号长度相同失败"
            assert result.get_input_username_value() == test_username, f"断言失败，输入用户名与获取用户名值不相同"
            result.input_password(test_password)
            assert len(result.get_input_password_text()) == len(test_password), f"断言密码长度相同失败"
            assert all(char in ['●', '*', '•'] for char in result.get_input_password_text()), "掩码字符不符合预期"
            result.click_return_button()
            assert result.get_cloud_name_text() == '网盘', f"返回网盘主页失败"
    
    @allure.story("用户输入密码显示明码再将密码恢复为掩码")
    @allure.title("验证密码明码变为掩码")
    def test_password_state_change_workflow(self, nut_cloud_login):
        with allure.step("密码明码变为掩码"):
            result = nut_cloud_login.input_password(test_password)
            assert len(result.get_input_password_text()) == len(test_password), f"断言密码长度相同失败"
            assert all(char in ['●', '*', '•'] for char in result.get_input_password_text()), "掩码字符不符合预期"
            result.click_password_display_button()
            assert result.get_input_password_text() == test_password, f"密码显示按钮点击失败"
            result.click_password_display_button()
            assert all(char in ['●', '*', '•'] for char in result.get_input_password_text()), "掩码字符不符合预期"
    
    @allure.step("用户输入正确的账号密码进行登录")
    @allure.title("验证正确用户名密码登陆成功")
    def test_input_username_password_login_success(self, nut_cloud_login, login_data):
        nut_cloud_login.set_skip_default_cleanup()
        
        def unbind_nut_cloud():
            logger.info("你还")
            home_page = HomePage(nut_cloud_login.driver)
            details_page = DetailsPage(nut_cloud_login.driver)
            account_information = AccountInformationPage(nut_cloud_login.driver)
            home_page.long_nut_cloud()
            details_page.click_account_button()
            account_information.unbind_nut_cloud_success()
            result._safe_navigate_back(1)
        
        nut_cloud_login.register_cleanup(unbind_nut_cloud)
        
        with allure.step("正确登录"):
            with allure.step("输入账号，输入密码"):
                result = nut_cloud_login.input_username(login_data['username'])
                assert len(result.get_input_username_text()) == len(login_data['username']), f"断言账号长度相同失败"
                assert result.get_input_username_value() == login_data[
                    'username'], f"断言失败，输入用户名与获取用户名值不相同"
                result.input_password(login_data['password'])
                assert len(result.get_input_password_text()) == len(login_data['password']), f"断言密码长度相同失败"
                assert all(char in ['●', '*', '•'] for char in result.get_input_password_text()), "掩码字符不符合预期"
            with allure.step("点击确定"):
                result.click_sure()
                login_success_toast = result.get_toast_page_text() == '成功绑定账号'
                assert login_success_toast, f"登录失败"
