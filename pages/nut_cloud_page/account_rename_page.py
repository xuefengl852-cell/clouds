import logging

from base.base_page import BasePage
from locators.account_rename_locators import AccountRenameLocators
from utils.loactor_validator import LocatorValidator

locators = AccountRenameLocators()
logger = logging.getLogger(__name__)
locator_validator = LocatorValidator()


class AccountRenamePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        logger.info(f"进入主页")
        locator_validator.validate(self)
    
    @property
    def account_name(self):
        return self.get_locator(locators.PAGE_SECTION, locators.ACCOUNT_INPUT)
    
    @property
    def delete_name(self):
        return self.get_locator(locators.PAGE_SECTION, locators.DELETE_NAME)
    
    @property
    def sure_button(self):
        return self.get_locator(locators.PAGE_SECTION, locators.SURE_BUTTON)
    
    @property
    def cancel_button(self):
        return self.get_locator(locators.PAGE_SECTION, locators.CANCEL_BUTTON)
    
    @property
    def bind_cloud(self):
        return self.get_locator(locators.PAGE_SECTION, locators.BIND_CLOUD)
    
    @property
    def tv_account(self):
        return self.get_locator(locators.PAGE_SECTION, locators.TV_ACCOUNT)
    
    def input_account_name(self, new_name: str):
        self.input_text(self.account_name, new_name, condition='visible')
        logger.info(f"账户名称输入值为：{new_name}")
        return self
    
    def click_delete_name(self):
        self.click(self.delete_name)
        return self
    
    def click_sure_button(self):
        self.click(self.sure_button)
        return self
    
    def click_cancel_button(self):
        self.click(self.cancel_button)
        return self
    
    def click_press_back_button(self):
        self.back()
        return self
    
    def verify_return_home(self):
        try:
            tv_account = self.wait_for_element(self.tv_account)
            return tv_account is not None
        except Exception as e:
            logger.error(f"导航到账户信息页面失败: {str(e)}")
            raise
        return self
    
    def verify_input_text(self):
        try:
            account_name = self.get_element_attribute(
                self.account_name,
                "text"
            )
            return account_name
        except Exception as e:
            logger.error(f"导航到账户信息页面失败: {str(e)}")
            raise
        return self
    
    def verify_home_cloud_name(self):
        try:
            account_name = self.get_element_attribute(
                self.tv_account,
                "text"
            )
            return account_name
        except Exception as e:
            logger.error(f"导航到账户信息页面失败: {str(e)}")
            raise
        return self
    
    def verify_rename_success_toast(self, toast):
        try:
            self.assert_toast(
                toast
            )
        except Exception as e:
            logger.error(f"导航到账户信息页面失败: {str(e)}")
            raise
        return self
    
    def assert_details_account_name(self, expect):
        account = self.get_text_by_id(self.tv_account)
        logger.info(f"账户名称文本值为：{account}")
        self.assert_text_is_equal(account, expect)
        return self
    
    def verify_input_account_name(self):
        try:
            account_name = self.get_element_attribute(
                self.account_name,
                "text"
            )
            return account_name
        except Exception as e:
            logger.error(f"导航到账户信息页面失败: {str(e)}")
            raise
        return self
