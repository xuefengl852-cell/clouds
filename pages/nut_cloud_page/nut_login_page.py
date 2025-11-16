import logging

import pytest
from selenium.common import TimeoutException

from base.base_page import BasePage
from locators.nut_login_locators import NutLoginLocators
from pages.nut_cloud_page.home_page import HomePage
from utils.loactor_validator import LocatorValidator
from utils.test_data_loader import load_test_data

logger = logging.getLogger(__name__)
locator_validator = LocatorValidator()
locators = NutLoginLocators()


class NutLoginPage(BasePage):
    # CONFIG_PATH = "data/locators/nut_login_page.yaml"
    # 定义配置节名称常量（与配置文件一致）
    
    def __init__(self, driver):
        super().__init__(driver)
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
    def bind_text(self):
        return self.get_locator(locators.PAGE_SECTION, locators.BIND_TEXT)
    
    @property
    def return_button(self):
        return self.get_locator(locators.PAGE_SECTION, locators.RETURN_BUTTON)
    
    @property
    def item_name(self):
        return self.get_locator(locators.PAGE_SECTION, locators.ITEM_NAME)
    
    @property
    def nut_cloud(self):
        return self.get_locator(locators.PAGE_SECTION, locators.NUT_CLOUD)
    
    @property
    def bind_cloud(self):
        return self.get_locator(locators.PAGE_SECTION, locators.BIND_CLOUD)
    
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
    
    def click_password_display_button(self):
        self.click(
            self.show_password
        )
        return self
    
    def click_sure(self):
        self.click(self.sure_button)
        return self
    
    def click_nut_cloud(self):
        try:
            self.click(self.nut_cloud)
        except Exception as e:
            logger.error(f"异常信息：{e}")
            raise
        return self
    
    def click_bind_cloud(self):
        try:
            self.click(self.bind_cloud)
        except Exception as e:
            logger.error(f"异常信息：{e}")
            raise
        return self
    
    def get_input_username_value(self):
        account = self.get_text_by_id(self.username_field)
        return account
    
    def get_toast_page_text(self):
        try:
            toast_text = self.get_toast_text()
            logger.info(f"{toast_text}")
            return toast_text
        except Exception as e:
            logger.error(f"异常信息：{e}")
    
    def get_input_password_text(self):
        try:
            password_value = self.get_element_attribute(
                self.password_field,
                "text"
            )
            return password_value
        except Exception as e:
            logger.error(f"异常信息：{e}")
    
    def get_input_username_text(self):
        try:
            password_value = self.get_element_attribute(
                self.username_field,
                "text"
            )
            return password_value
        except Exception as e:
            logger.error(f"异常信息：{e}")
    
    def get_cloud_name_text(self):
        try:
            cloud_name_value = self.get_element_attribute(
                self.bind_text,
                "text"
            )
            logger.info(f"获取返回登录页面按钮文本：{cloud_name_value}")
            return cloud_name_value
        except Exception as e:
            logger.error(f"异常信息：{e}")
    
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
        try:
            # 获取有效凭证
            login_data = self.get_valid_credentials('login_data_positive.json')
            
            # 1. 初始化登录页面
            username = login_data["username"]
            password = login_data["password"]
            # 第一步: 输入凭据
            self.input_username(username)
            self.input_password(password)
            self.click_sure()
            try:
                if self.get_toast_page_text() == '成功绑定账号':
                    home_page = HomePage(self.driver)
                    return home_page
            except TimeoutException:
                logger.error("登录失败，未看到成功提示")
                # 可以在这里添加截屏等诊断信息
                raise Exception("登录操作未在预期时间内完成")
        except Exception as e:
            logger.error(f"异常信息：{e}")
            raise
    
    def logged_in_successful(self):
        try:
            self.click_bind_cloud()
            self.click_nut_cloud()
        except TimeoutException:
            logger.error("登录失败，未看到成功提示")
            # 可以在这里添加截屏等诊断信息
            raise Exception("登录操作未在预期时间内完成")
