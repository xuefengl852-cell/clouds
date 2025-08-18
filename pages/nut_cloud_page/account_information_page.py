import logging

from base.base_page import BasePage
from locators.account_information_locators import AccountInformationLocators
from utils.loactor_validator import LocatorValidator

locators = AccountInformationLocators()
locator_validator = LocatorValidator()
logger = logging.getLogger(__name__)


class AccountInformationPage(BasePage):
    @property
    def return_button(self):
        return self.get_locator(locators.PAGE_SECTION, locators.RETURN_BUTTON)
    
    @property
    def edit_button(self):
        return self.get_locator(locators.PAGE_SECTION, locators.EDIT_BUTTON)
    
    @property
    def unbind_button(self):
        return self.get_locator(locators.PAGE_SECTION, locators.UNBIND_BUTTON)
    
    @property
    def assert_bind_cloud(self):
        return self.get_locator(locators.PAGE_SECTION, locators.BIND_CLOUD)
    
    @property
    def assert_account_input(self):
        return self.get_locator(locators.PAGE_SECTION, locators.ACCOUNT_INPUT)
    
    @property
    def assert_unbind_title(self):
        return self.get_locator(locators.PAGE_SECTION, locators.UNBIND_TITLE)
    
    def click_return_button(self):
        try:
            self.click(self.return_button)
        except Exception as e:
            logger.warning(f"未找到当前元素：{e}")
    
    def click_edit_button(self):
        try:
            self.click(self.edit_button)
        except Exception as e:
            logger.warning(f"未找到当前元素：{e}")
    
    def click_unbind_button(self):
        try:
            self.click(self.unbind_button)
        except Exception as e:
            logger.warning(f"未找到当前元素：{e}")
    
    def assert_click_return_button(self):
        try:
            assert self.find_by_id(self.assert_bind_cloud), f"返回主页失败"
        except Exception as e:
            logger.warning(f"验证失败，未找到当前元素：{e}")
            raise
    
    def assert_click_edit_button(self):
        try:
            assert self.find_by_id(self.assert_account_input), f"进入账户编辑页失败"
        except Exception as e:
            logger.warning(f"验证失败，未找到当前元素：{e}")
            raise
    
    def assert_click_unbind_button(self):
        try:
            assert self.find_by_id(self.assert_unbind_title), f"进入解绑提示页失败"
        except Exception as e:
            logger.warning(f"验证失败，未找到当前元素：{e}")
            raise
