import logging

import allure
from selenium.common import NoSuchElementException

from base.base_page import BasePage
from locators.home_locators import HomeLocators
from pages.clouds_more_page import CloudsMorePage
from pages.nut_cloud_page.details_page import DetailsPage
from utils.loactor_validator import LocatorValidator

locators = HomeLocators()
locator_validator = LocatorValidator()
logger = logging.getLogger(__name__)


class HomePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        logger.info(f"进入主页")
        locator_validator.validate(self)
    
    @property
    def return_button(self):
        return self.get_locator(locators.PAGE_SECTION, locators.RETURN_BUTTON)
    
    @property
    def bind_cloud(self):
        return self.get_locator(locators.PAGE_SECTION, locators.BIND_CLOUD)
    
    @property
    def nut_cloud(self):
        return self.get_locator(locators.PAGE_SECTION, locators.NUT_CLOUD)
    
    @property
    def view_more(self):
        return self.get_locator(locators.PAGE_SECTION, locators.VIEW_MORE)
    
    @property
    def iv_prepage(self):
        return self.get_locator(locators.PAGE_SECTION, locators.IV_PREPAGE)
    
    @property
    def iv_nextpage(self):
        return self.get_locator(locators.PAGE_SECTION, locators.IV_NEXTPAGE)
    
    @property
    def bind_cloud_window(self):
        return self.get_locator(locators.PAGE_SECTION, locators.BIND_CLOUD_WINDOWS)
    
    @property
    def more_view_window(self):
        return self.get_locator(locators.PAGE_SECTION, locators.MORE_VIEW_WINDOW)
    
    @property
    def nut_file_id(self):
        return self.get_locator(locators.PAGE_SECTION, locators.NUT_FILE_ID)
    
    def long_press_cloud_fixture(self):
        """使用登录页传递的driver检查主页元素"""
        try:
            details_page = DetailsPage(self.driver)
            self.long_press(self.nut_cloud)
            return details_page
        except Exception as e:
            logger.warning(f"检查主页元素失败：{e}")
            return self
    
    def long_nut_cloud(self):
        """使用登录页传递的driver检查主页元素"""
        self.long_press(self.nut_cloud)
        return self
    
    def click_bind_cloud(self):
        self.click(self.bind_cloud)
        return self
    
    def click_more_button(self):
        self.click(self.view_more)
        return self
    
    def click_cloud(self):
        self.click(self.nut_cloud)
        return self
    
    @allure.step("点击左翻页按钮")
    def click_return_button(self):
        try:
            self.click(self.iv_prepage)
            return True
        except Exception as e:
            logger.warning(f"检查主页元素失败：{e}")
            return False
    
    @allure.step("点击右翻页按钮")
    def click_return_button(self):
        try:
            self.click(self.iv_nextpage)
            return True
        except Exception as e:
            logger.warning(f"检查主页元素失败：{e}")
            return False
    
    def assert_enter_details(self):
        try:
            self.wait_for_element(
                self.bind_cloud_window
            )
            return True
        except NoSuchElementException as e:
            logger.error(f"元素定位失败: {str(e)}")
            return False
    
    def assert_bind_cloud_window(self):
        try:
            self.wait_for_element(
                self.bind_cloud_window
            )
            return True
        except NoSuchElementException as e:
            logger.error(f"元素定位失败: {str(e)}")
            return False
    
    def assert_more_window(self):
        try:
            self.wait_for_element(
                self.more_view_window
            )
            return True
        except AssertionError as e:
            logger.error(f"元素定位失败: {str(e)}")
            return False
    
    def assert_click_enter_nut_cloud(self, text='我的坚果云'):
        try:
            self.is_resource_id_text_visible(
                self.nut_file_id,
                text
            )
            return True
        except AssertionError as e:
            logger.error(f"元素断言失败: {str(e)}")
            return False
    
    def click_more_button_workflow(self):
        try:
            cloud_more_page = CloudsMorePage(self.driver)
            result = self.click(self.view_more)
            assert result.assert_more_window(), f"进入更多弹窗失败"
            return cloud_more_page
        except Exception as e:
            logger.error(f"点击更多按钮失败：{e}")
