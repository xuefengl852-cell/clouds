import logging

from base.base_page import BasePage
from locators.details_locators import DetailsLocators
from pages.nut_cloud_page.account_information_page import AccountInformationPage
from pages.nut_cloud_page.account_rename_page import AccountRenamePage
from utils.loactor_validator import LocatorValidator

locators = DetailsLocators()
locator_validator = LocatorValidator()
logger = logging.getLogger(__name__)


class DetailsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        logger.info(f"进入主页")
        locator_validator.validate(self)
    
    @property
    def close_button(self):
        return self.get_locator(locators.PAGE_SECTION, locators.CLOSE_BUTTON)
    
    @property
    def rename_button(self):
        return self.get_locator(locators.PAGE_SECTION, locators.RENAME_BUTTON)
    
    @property
    def account_button(self):
        return self.get_locator(locators.PAGE_SECTION, locators.ACCOUNT_BUTTON)
    
    @property
    def nut_cloud(self):
        return self.get_locator(locators.PAGE_SECTION, locators.NUT_CLOUD)
    
    @property
    def account_unbind(self):
        return self.get_locator(locators.PAGE_SECTION, locators.ACCOUNT_UNBIND)
    
    @property
    def rename_window(self):
        return self.get_locator(locators.PAGE_SECTION, locators.RENAME_WINDOW)
    
    def click_close_button(self):
        try:
            self.click(self.close_button)
        except Exception as e:
            logger.warning(f"未找到当前元素：{e}")
    
    def click_account_button(self):
        try:
            self.click(self.account_button)
        except Exception as e:
            logger.warning(f"未找到当前元素：{e}")
    
    def click_rename_button(self):
        try:
            self.click(self.rename_button)
        except Exception as e:
            logger.warning(f"未找到当前元素：{e}")
    
    def assert_click_rename_button(self):
        try:
            self.find_by_id(self.rename_window)
            return True
        except Exception as e:
            logger.warning(f"未找到当前元素：{e}")
            return False
    
    def assert_click_account_button(self):
        try:
            self.find_by_id(self.account_unbind)
            return True
        except Exception as e:
            logger.warning(f"未找到当前元素：{e}")
            return False
    
    def assert_click_close_button(self):
        try:
            self.find_by_id(self.nut_cloud)
            return True
        except Exception as e:
            logger.warning(f"元素定位失败：{e}")
            return False
    
    def navigate_to_account_information(self):
        try:
            self.click_account_button()
            if self.assert_click_account_button():
                logger.info(f"已返回到账户信息页")
                return AccountInformationPage(self.driver)
        except Exception as e:
            logger.error(f"导航到账户信息页面失败: {str(e)}")
            raise RuntimeError(f"无法导航到账户信息页面: {str(e)}")
            return self
    
    def navigate_to_account_rename(self):
        try:
            self.click_rename_button()
            if self.assert_click_rename_button():
                logger.info(f"已返回到账户信息页")
                return AccountRenamePage(self.driver)
        except Exception as e:
            logger.error(f"导航到账户信息页面失败: {str(e)}")
            raise RuntimeError(f"无法导航到账户信息页面: {str(e)}")
            return self
