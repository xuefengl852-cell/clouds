import logging

import pytest

from base.base_page import BasePage
from locators.login_locators import LoginLocators
from pages.nut_cloud_page.home_page import HomePage
from utils.loactor_validator import LocatorValidator
from utils.test_data_loader import load_test_data

logger = logging.getLogger(__name__)
locator_validator = LocatorValidator()
locators = LoginLocators()


class LoginPage(BasePage):
    # CONFIG_PATH = "data/locators/login_page.yaml"
    # 定义配置节名称常量（与配置文件一致）
    
    def __init__(self, driver):
        super().__init__(driver)
        logger.info(f"初始化登录页面: {self.__class__.__name__}")
        # 验证必需的定位器配置
        locator_validator.validate(self)
    
    # 页面元素访问器（更新为与配置文件匹配的键名）
    @property
    def home_bind(self):
        return self.get_locator(locators.PAGE_SECTION, locators.HOME_BIND)
    
    @property
    def username_field(self):
        return self.get_locator(locators.PAGE_SECTION, locators.USERNAME_FIELD)
    
    @property
    def password_field(self):
        return self.get_locator(locators.PAGE_SECTION, locators.PASSWORD_FIELD)
    
    @property
    def show_password(self):
        return self.get_locator(locators.PAGE_SECTION, locators.SHOW_PASSWORD)
    
    @property
    def sure_button(self):
        return self.get_locator(locators.PAGE_SECTION, locators.SURE_BUTTON)
    
    @property
    def cancel_button(self):
        return self.get_locator(locators.PAGE_SECTION, locators.CANCEL_BUTTON)
    
    @property
    def return_button(self):
        return self.get_locator(locators.PAGE_SECTION, locators.RETURN_BUTTON)
        return self
    
    def click_return_button(self):
        self.click(self.return_button)
        return self
    
    def click_cancel_button(self):
        self.click(self.cancel_button)
        return self
    
    def input_username(self, username):
        self.input_text(self.username_field, username)
        return self
    
    def input_password(self, password):
        self.input_text(self.password_field, password)
        return self
    
    def test_initial_password_state(self):
        self.assert_password_display_state(
            locator=self.password_field,
            expected_state='masked',
        )
    
    def click_password_display_button(self):
        self.click(
            self.show_password
        )
        return self
    
    def click_sure(self):
        self.click(self.sure_button)
        return self
    
    def verify_success_login(self):
        """验证成功登录状态"""
        try:
            # 直接调用断言方法，无需额外assert
            self.assert_toast("成功绑定账号")
            logger.info("✅ 登录成功验证通过")
            return True
        except AssertionError as e:
            # 捕获assert_toast抛出的AssertionError
            logger.error(f"❌ 登录成功验证失败: {str(e)}")
            return False
        except Exception as e:
            # 捕获其他意外异常
            logger.exception(f"❗ 登录验证过程中发生未预期错误: {str(e)}")
            return False
    
    @staticmethod
    def get_valid_credentials(test_data_path):
        test_data = load_test_data(test_data_path)
        if not test_data:
            pytest.fail("❌ 未找到有效的登录凭证")
        return next(
            data for data in test_data
            if data["expected_result"] is True
        )
    
    def login_successful(self):
        from pages.home_clouds_page import HomeCloudsPage
        # 获取有效凭证
        login_data = self.get_valid_credentials('login_data_positive.json')
        # 1. 初始化登录页面
        username = login_data["username"]
        password = login_data["password"]
        nut_cloud_page = HomeCloudsPage(self.driver)
        nut_cloud_page.click_nut_cloud_login_successful()
        # 第一步: 输入凭据
        self. \
            input_username(username) \
            .input_password(password) \
            .click_sure() \
            .verify_success_login()
        # 第三步: 验证登录成功
        if self.verify_success_login():
            home_page = HomePage(self.driver)
            logger.info("✅ 登录成功，导航到主页")
            return home_page
        else:
            logger.warning("❌ 登录验证失败")
            return self
            logger.info(f"登录后返回的页面类型: {type(home_page)}")
    
    def assert_input_username(self, expect):
        account = self.get_text_by_id(self.username_field)
        logger.info(f"账户名称文本值为：{account}")
        self.assert_text_is_equal(account, expect)
        return self
    
    def assert_password_visible(self, password_text='请输入应用密码'):
        """验证密码明文可见状态"""
        self.assert_password_plain(
            locator=self.password_field,
            expected_text=password_text
        )
        return self
    
    def assert_password_hidden(self):
        """验证密码掩码状态"""
        self.assert_password_masked(
            locator=self.password_field
        )
        return self
    
    def assert_click_return_button_home(self):
        self.assert_element_visible(self.home_bind)
    
    def assert_toast_nut(self, message='请输入您的账号'):
        self.assert_toast(message)
        return self
