import logging

from base.base_page import BasePage
from locators.document_home_locators import DocumentHomeLocators
from utils.loactor_validator import LocatorValidator

locators = DocumentHomeLocators()
locator_validator = LocatorValidator()
logger = logging.getLogger(__name__)


class DocumentHomePage(BasePage):
    
    def __init__(self, driver):
        super().__init__(driver)
        logger.info(f"进入主页")
        locator_validator.validate(self)
    
    @property
    def return_button(self):
        return self.get_locator(locators.PAGE_SECTION, locators.DRIVE)
    
    @property
    def search(self):
        return self.get_locator(locators.PAGE_SECTION, locators.SEARCH)
    
    @property
    def download(self):
        return self.get_locator(locators.PAGE_SECTION, locators.DOWNLOAD)
    
    @property
    def refresh(self):
        return self.get_locator(locators.PAGE_SECTION, locators.REFRESH)
    
    @property
    def setup(self):
        return self.get_locator(locators.PAGE_SECTION, locators.SETUP)
    
    @property
    def jan_grid_chb(self):
        return self.get_locator(locators.PAGE_SECTION, locators.JAN_GRID_CHB)
    
    @property
    def jan_grid_tv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.JAN_GRID_TV)
    
    @property
    def file_grid_tv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.FILE_GRID_TV)
    
    @property
    def jan_list_name_tv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.JAN_LIST_NAME_TV)
    
    @property
    def dd_drive(self):
        return self.get_locator(locators.PAGE_SECTION, locators.DD_DRIVE)
    
    @property
    def root_layout(self):
        return self.get_locator(locators.PAGE_SECTION, locators.ROOT_LAYOUT)
    
    @property
    def status_grid_tv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.STATUS_GRID_TV)
    
    @property
    def pre_page(self):
        return self.get_locator(locators.PAGE_SECTION, locators.PRE_PAGE)
    
    @property
    def next_page(self):
        return self.get_locator(locators.PAGE_SECTION, locators.NEXT_PAGE)
    
    @property
    def page_tv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.PAGE_TV)
    
    @property
    def tv_account(self):
        return self.get_locator(locators.PAGE_SECTION, locators.TV_ACCOUNT)
    
    @property
    def drive(self):
        return self.get_locator(locators.PAGE_SECTION, locators.DRIVE)
    
    def click_return_button(self):
        try:
            self.click(self.drive)
        except Exception as e:
            logger.error(f"异常信息：{e}")
        return self
    
    def verify_return_cloud_home_page(self):
        try:
            tv_account = self.wait_for_element(self.tv_account)
            return tv_account is not None
        except Exception as e:
            logger.error(f"异常信息：{e}")
            return False
        return self
    
    def click_search_button(self):
        try:
            self.click(self.search)
        except Exception as e:
            logger.error(f"异常信息：{e}")
        return self
    
    def verify_search_content_same(self):
        try:
            search_file = self.get_all_folder_texts(self.jan_list_name_tv)
            return search_file
        except Exception as e:
            logger.error(f"异常信息：{e}")
        return self
    
    def get_all_document_names(self):
        """获取主页所有文档名称"""
        return self.get_paginated_data(
            page_indicator_locator=self.page_tv,  # 页码指示器元素
            section=locators.PAGE_SECTION,
            key=locators.FILE_GRID_TV,
            next_button_locator=self.next_page
        )
    
    def get_all_search_document_names(self):
        """获取搜索所有文档名称"""
        self.click(self.search)
        return self.get_paginated_data(
            page_indicator_locator=self.page_tv,  # 页码指示器元素
            section=locators.PAGE_SECTION,
            key=locators.JAN_LIST_NAME_TV,
            next_button_locator=self.next_page
        )
