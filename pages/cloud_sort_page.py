import logging

from base.base_page import BasePage
from locators.cloud_sort_locators import CloudSortLocators
from utils.loactor_validator import LocatorValidator

logger = logging.getLogger(__name__)
locator_validator = LocatorValidator()
locators = CloudSortLocators()


class CloudSortPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # 验证必需的定位器配置
        locator_validator.validate(self)
    
    @property
    def add_time(self):
        return self.get_locator(locators.PAGE_SECTION, locators.ADD_TIME)
    
    @property
    def name(self):
        return self.get_locator(locators.PAGE_SECTION, locators.NAME)
    
    @property
    def type(self):
        return self.get_locator(locators.PAGE_SECTION, locators.TYPE)
    
    @property
    def asc_order(self):
        return self.get_locator(locators.PAGE_SECTION, locators.ASC)
    
    @property
    def desc_order(self):
        return self.get_locator(locators.PAGE_SECTION, locators.DESC)
    
    @property
    def cloud_return(self):
        return self.get_locator(locators.PAGE_SECTION, locators.CLOUD)
    
    @property
    def cancel(self):
        return self.get_locator(locators.PAGE_SECTION, locators.CANCEL)
    
    @property
    def sure(self):
        return self.get_locator(locators.PAGE_SECTION, locators.SURE)
    
    def click_add_time(self):
        try:
            self.click(self.add_time)
        except Exception as e:
            logger.error(f"异常信息：{e}")
            raise
        return self
    
    def click_name(self):
        try:
            self.click(self.name)
        except Exception as e:
            logger.error(f"异常信息：{e}")
            raise
        return self
    
    def click_type(self):
        try:
            self.click(self.type)
        except Exception as e:
            logger.error(f"异常信息：{e}")
            raise
        return self
    
    def click_asc_order(self):
        try:
            self.click(self.asc_order)
        except Exception as e:
            logger.error(f"异常信息：{e}")
            raise
        return self
    
    def click_desc_order(self):
        try:
            self.click(self.desc_order)
        except Exception as e:
            logger.error(f"异常信息：{e}")
            raise
        return self
    
    def click_cancel(self):
        try:
            self.click(self.cancel)
        except Exception as e:
            logger.error(f"异常信息：{e}")
            raise
        return self
    
    def click_sure(self):
        try:
            self.click(self.sure)
        except Exception as e:
            logger.error(f"异常信息：{e}")
            raise
        return self
    
    def get_add_time_button_clickable(self):
        try:
            add_time = self.get_input_value_by_id(
                self.add_time,
                "clickable"
            )
            logger.info(f"{type(add_time)}")
            return add_time
        except Exception as e:
            raise
    
    def get_name_button_clickable(self):
        try:
            name = self.get_input_value_by_id(
                self.name,
                "clickable"
            )
            return name
        except Exception as e:
            raise
    
    def get_type_button_clickable(self):
        try:
            type_value = self.get_input_value_by_id(
                self.type,
                "clickable"
            )
            return type_value
        except Exception as e:
            raise
    
    def get_asc_order_button_clickable(self):
        try:
            asc_order = self.get_input_value_by_id(
                self.asc_order,
                "clickable"
            )
            return asc_order
        except Exception as e:
            logger.error(f"异常信息：{e}")
            raise
    
    def get_desc_order_button_clickable(self):
        try:
            desc_order = self.get_input_value_by_id(
                self.desc_order,
                "clickable"
            )
            return desc_order
        except Exception as e:
            logger.error(f"异常信息：{e}")
            raise
    
    def verify_click_cancel_success(self):
        try:
            element = self.wait_for_element(
                self.cloud_return
            )
            return element is not None
        except Exception as e:
            logger.error(f"异常信息：{e}")
            raise
