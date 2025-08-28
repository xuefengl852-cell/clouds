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
    def bind_cloud(self):
        return self.get_locator(locators.PAGE_SECTION, locators.BIND_CLOUD)
    
    @property
    def account_rename(self):
        return self.get_locator(locators.PAGE_SECTION, locators.ACCOUNT_RENAME)
    
    @property
    def unbind_title(self):
        return self.get_locator(locators.PAGE_SECTION, locators.UNBIND_TITLE)
    
    @property
    def sure_button(self):
        return self.get_locator(locators.PAGE_SECTION, locators.SURE_BUTTON)
    
    @property
    def cancel_button(self):
        return self.get_locator(locators.PAGE_SECTION, locators.CANCEL_BUTTON)
    
    @property
    def nut_cloud_bind(self):
        return self.get_locator(locators.PAGE_SECTION, locators.NUT_CLOUD_BIND)
    
    def click_return_button(self):
        try:
            self.click(self.return_button)
        except Exception as e:
            logger.warning(f"未找到当前元素：{e}")
        return self
    
    def click_edit_button(self):
        try:
            self.click(self.edit_button)
        except Exception as e:
            logger.error(f"未找到当前元素：{e}")
        return self
    
    def click_unbind_button(self):
        try:
            self.click(self.unbind_button)
        except Exception as e:
            logger.error(f"未找到当前元素：{e}")
        return self
    
    def click_unbind_sure_button(self):
        try:
            self.click(self.sure_button)
        except Exception as e:
            logger.error(f"未找到当前元素：{e}")
        return self
    
    def click_unbind_cancel_button(self):
        try:
            self.click(self.cancel_button)
        except Exception as e:
            logger.error(f"未找到当前元素：{e}")
        return self
    
    def get_bind_cloud_text(self):
        try:
            bind_cloud_text = self.get_input_value_by_id(
                self.bind_cloud,
                "text"
            )
            return bind_cloud_text
        except Exception as e:
            logger.warning(f"验证失败，未找到当前元素：{e}")
            raise
    
    def get_account_rename_text(self):
        try:
            account_rename_text = self.get_input_value_by_id(
                self.account_rename,
                "text"
            )
            return account_rename_text
        except Exception as e:
            logger.warning(f"验证失败，未找到当前元素：{e}")
            raise
    
    def get_unbind_window_text(self):
        try:
            unbind_window_text = self.get_input_value_by_id(
                self.unbind_title,
                "text"
            )
            return unbind_window_text
        except Exception as e:
            logger.warning(f"验证失败，未找到当前元素：{e}")
            raise
    
    def verify_return_account(self):
        try:
            element = self.wait_for_element(
                self.return_button
            )
            return element is not None
        except Exception as e:
            logger.error(f"验证失败，未找到当前元素：{e}")
            return False
            raise
        return self
    
    def verify_unbind_success(self):
        try:
            element = self.wait_for_element(
                self.nut_cloud_bind
            )
            return element is not None
        except Exception as e:
            logger.error(f"验证失败，未找到当前元素：{e}")
            return False
            raise
        return self
