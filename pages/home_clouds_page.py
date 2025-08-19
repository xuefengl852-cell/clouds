import logging

from selenium.common import TimeoutException

from base.base_page import BasePage
from locators.home_clouds_locators import HomeCloudsLocators
from services.logout_services import locator_validator
from utils.test_data_loader import load_test_data

locators = HomeCloudsLocators()
cloud_index_data = load_test_data("home_clouds.json")
logger = logging.getLogger(__name__)


def get_cloud_index(cloud_type):
    for cloud in cloud_index_data:
        if cloud['cloud_type'] == cloud_type:
            return cloud['index']


class HomeCloudsPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # 验证必需的定位器配置
        locator_validator.validate(self)
    
    @property
    def public_resource_id_locator(self):
        return self.get_locator(locators.PAGE_SECTION, locators.PUBLIC_RESOURCE_ID)
    
    @property
    def onedrive_home_id_locator(self):
        return self.get_locator(locators.PAGE_SECTION, locators.ONEDRIVE_HOME_ID)
    
    @property
    def aliyun_home_id_locator(self):
        return self.get_locator(locators.PAGE_SECTION, locators.ALIYUN_HOME_ID)
    
    @property
    def nut_webdav_home_id_locator(self):
        return self.get_locator(locators.PAGE_SECTION, locators.NUT_WEBDAV_HOME_CLOUD_ID)
    
    @property
    def baidu_home_id_locator(self):
        return self.get_locator(locators.PAGE_SECTION, locators.BAIDU_HOME_CLOUD_ID)
    
    def click_nut_cloud(self, index):
        self.click_by_locator_index(
            self.public_resource_id_locator,
            index
        )
        return self
    
    def is_cloud_home_resource_id_visible(self, cloud_type, timeout=3):
        try:
            # if cloud_type == 'onedrive' | 'aliyun':
            #     time.sleep(timeout)
            #     return cloud_index_data['cloud_id']
            element_value = self.get_element_attribute(
                self.get_home_id_locator(cloud_type),
                "text"
            )
            logger.info(f"{element_value}")
            return element_value
        
        except TimeoutException:
            logger.error(f"等待 {cloud_type} 主页元素超时")
        return self
    
    def get_home_id_locator(self, cloud_type):
        """根据网盘类型返回对应的资源ID定位器"""
        locator_mapping = {
            "onedrive": self.onedrive_home_id_locator,
            "aliyun": self.aliyun_home_id_locator,
            "nut_cloud": self.nut_webdav_home_id_locator,
            "webdav": self.nut_webdav_home_id_locator,
            "baidu": self.baidu_home_id_locator
        }
        return locator_mapping.get(cloud_type.lower())
