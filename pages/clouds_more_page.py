import logging

from selenium.common import TimeoutException, NoSuchElementException

from base.base_page import BasePage
from locators.clouds_more_locators import CloudsMoreLocators
from utils.loactor_validator import LocatorValidator

locator_validator = LocatorValidator()
logger = logging.getLogger(__name__)
locators = CloudsMoreLocators()


class CloudsMorePage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        logger.info(f"进入主页更多选项弹窗")
        locator_validator.validate(self)
    
    @property
    def tv_display(self):
        return self.get_locator(locators.PAGE_SECTION, locators.TV_DISPLAY)
    
    @property
    def tv_sort(self):
        return self.get_locator(locators.PAGE_SECTION, locators.TV_SORT)
    
    @property
    def rl_one(self):
        return self.get_locator(locators.PAGE_SECTION, locators.RL_ONE)
    
    def click_view_button(self):
        self.click(self.tv_display)
        return self
    
    def click_list_button(self):
        self.click(self.tv_display)
    
    def click_sort_button(self):
        self.click(self.tv_sort)
        return self
    
    def get_display_text_value(self, attribute_name):
        """
        断言主页状态
        :return:
        """
        return self.get_input_value_by_id(self.tv_display, attribute_name)
    
    def is_switch_view_visible(self, text='视图模式'):
        """
        断言弹窗文本
        :param text:
        :return:
        """
        try:
            self.is_resource_id_text_visible(
                self.tv_display,
                text
            )
            return True
        except (TimeoutException, NoSuchElementException):
            return False
        except Exception as e:
            logger.error(f"检查元素可见性时出错: {str(e)}")
            return False
