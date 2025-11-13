import logging

from base.base_page import BasePage
from locators.document_home_locators import DocumentHomeLocators
from pages.nut_cloud_page.document_home_page import hardware_version
from utils.loactor_validator import LocatorValidator

logger = logging.getLogger(__name__)
locator_validator = LocatorValidator()
locators = DocumentHomeLocators()


class FilePage(BasePage):
    CONFIG_PATH = "data/locators/document_home_page.yaml"
    
    def __init__(self, driver):
        super().__init__(driver)
        logger.info(f"文件夹页面")
        locator_validator.validate(self)
    
    @property
    def return_button(self):
        return self.get_locator(locators.PAGE_SECTION, locators.BACK)
    
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
    def dialog_title(self):
        return self.get_locator(locators.PAGE_SECTION, locators.DIALOG_TITLE)
    
    @property
    def cover_file_tv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.COVER_FILE_TV)
    
    @property
    def detail_grid_view(self):
        return self.get_locator(locators.PAGE_SECTION, locators.DETAIL_GRID_VIEW)
    
    @property
    def pre_page(self):
        return self.get_locator(locators.PAGE_SECTION, locators.PRE_PAGE)
    
    @property
    def tv_drive(self):
        return self.get_locator(locators.PAGE_SECTION, locators.TV_DRIVE)
    
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
    def jan_pop_sort(self):
        return self.get_locator(locators.PAGE_SECTION, locators.JAN_POP_SORT)
    
    @property
    def document_parent_element(self):
        return self.get_locator(locators.PAGE_SECTION, locators.DOCUMENT_PARENT_ELEMENT)
    
    @property
    def jan_search_et(self):
        return self.get_locator(locators.PAGE_SECTION, locators.JAN_SEARCH_ET)
    
    @property
    def name_file_tv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.NAME_FILE_TV)
    
    @property
    def file_grid_tv_id(self):
        return self.get_locator(locators.PAGE_SECTION, locators.FILE_GRID_TV_ID)
    
    @property
    def select_ed(self):
        return self.get_locator(locators.PAGE_SECTION, locators.SELECT_ED)
    
    @property
    def jan_new_file_tv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.JAN_NEW_FILE_TV)
    
    @property
    def ja_document_name_iv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.JA_DOCUMENT_NAME_IV)
    
    @property
    def title_file_tv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.TITLE_FILE_TV)
    
    @property
    def type_file_tv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.TYPE_FILE_TV)
    
    @property
    def size_file_tv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.SIZE_FILE_TV)
    
    @property
    def time_file_tv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.TIME_FILE_TV)
    
    @property
    def item_name_tv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.ITEM_NAME_TV)
    
    @property
    def dialog_close(self):
        return self.get_locator(locators.PAGE_SECTION, locators.DIALOG_CLOSE)
    
    def get_all_document_names(self):
        """获取主页所有文档名称"""
        return self.get_paginated_data(
            page_indicator_locator=self.page_tv,  # 页码指示器元素
            section=locators.PAGE_SECTION,
            key=locators.FILE_GRID_TV,
            next_button_locator=self.next_page
        )
    
    def click_search_button(self):
        try:
            self.click(self.search)
        except Exception as e:
            logger.error(f"异常信息：{e}")
        return self
    
    def get_all_search_document_names(self):
        """获取搜索所有文档名称"""
        return self.get_paginated_data(
            page_indicator_locator=self.page_tv,  # 页码指示器元素
            section=locators.PAGE_SECTION,
            key=locators.JAN_LIST_NAME_TV,
            next_button_locator=self.next_page
        )
    
    def verify_enter_search_page(self):
        search_text = self.get_element_attribute(
            self.jan_search_et,
            "text"
        )
        return search_text
    
    def click_transmission_button(self):
        try:
            self.click(self.download)
        except Exception as e:
            logger.error(f"异常信息：{e}")
        return self
    
    def verify_click_enter_transmission_list(self):
        try:
            transmission_list_return_text = self.get_element_attribute(
                self.dd_drive,
                "text"
            )
            return transmission_list_return_text
        except Exception as e:
            logger.error(f"异常信息：{e}")
    
    def click_refresh_button(self):
        try:
            self.click(self.refresh)
        except Exception as e:
            logger.error(f"异常信息：{e}")
        return self
    
    def click_more_button(self):
        try:
            self.click(self.setup)
        except Exception as e:
            logger.error(f"异常信息{e}")
        return self
    
    def get_new_file_text(self):
        try:
            title_text = self.get_element_attribute(
                self.jan_new_file_tv,
                "text"
            )
            return title_text
        except Exception as e:
            logger.error(f"异常信息：{e}")
            raise
    
    class MorePopWindow(BasePage):
        CONFIG_PATH = "data/locators/document_home_page.yaml"
        
        def __init__(self, driver):
            super().__init__(driver)
        
        @property
        def list_mode(self):
            return self.get_locator(locators.PAGE_SECTION, locators.LIST_MODE)
        
        @property
        def phone_ja_copy(self):
            return self.get_locator(locators.PAGE_SECTION, locators.PHONE_JA_COPY)
        
        @property
        def select_ed(self):
            return self.get_locator(locators.PAGE_SECTION, locators.SELECT_ED)
        
        @property
        def phone_select(self):
            return self.get_locator(locators.PAGE_SECTION, locators.PHONE_SELECT)
        
        @property
        def phone_ja_move(self):
            return self.get_locator(locators.PAGE_SECTION, locators.PHONE_JA_MOVE)
        
        @property
        def phone_jan_sec(self):
            return self.get_locator(locators.PAGE_SECTION, locators.PHONE_JAN_SEC)
        
        @property
        def phone_jan_delete(self):
            return self.get_locator(locators.PAGE_SECTION, locators.PHONE_JAN_DELETE)
        
        @property
        def root_layout(self):
            return self.get_locator(locators.PAGE_SECTION, locators.ROOT_LAYOUT)
        
        @property
        def return_button(self):
            return self.get_locator(locators.PAGE_SECTION, locators.BACK)
        
        @property
        def jan_new_file_tv(self):
            return self.get_locator(locators.PAGE_SECTION, locators.JAN_NEW_FILE_TV)
        
        def click_specify_coordinates(self, coordinates_data):
            """
            点击更多popWindow弹出位置的新建文件夹
            :param coordinates_data: 元素坐标文件
            :return self:
            """
            try:
                if hardware_version in coordinates_data:
                    config = coordinates_data[hardware_version]
                    self.click_through_coordinates(
                        x=config['x'],
                        y=config['y']
                    )
                else:
                    logger.warning(f"未找到对应设备的硬件版本号，请重试")
            except Exception as e:
                logger.error(f"异常信息：{e}")
                raise
            return self
        
        def verify_switch_list_mode_success(self):
            """验证切换列表模式成功"""
            try:
                list_mode_logo = self.wait_for_element(
                    self.list_mode
                )
                return list_mode_logo is not None
            except Exception as e:
                logger.error(f"异常信息：{e}")
                return False
        
        def verify_switch_view_mode_success(self):
            """验证切换列表模式成功"""
            try:
                view_mode_logo = self.wait_for_element(
                    self.root_layout
                )
                return view_mode_logo is not None
            except Exception as e:
                logger.error(f"异常信息：{e}")
                return False
        
        def verify_click_batch_management_success(self):
            try:
                elements = [
                    self.wait_for_element(self.phone_ja_copy),
                    self.wait_for_element(self.select_ed),
                    self.wait_for_element(self.phone_select),
                    self.wait_for_element(self.phone_ja_move),
                    self.wait_for_element(self.phone_jan_sec),
                    self.wait_for_element(self.phone_jan_delete)
                ]
                return all(element is not None for element in elements)
            except Exception as e:
                logger.error(f"异常信息：{e}")
                return False
        
        def click_batch_management_return(self):
            try:
                self.click(self.select_ed)
            except Exception as e:
                logger.error(f"异常信息：{e}")
                raise
            return self
        
        def verify_click_sort_success(self):
            try:
                sort_text = self.get_element_attribute(
                    self.jan_new_file_tv,
                    "text"
                )
                return sort_text
            except Exception as e:
                logger.error(f"异常信息：{e}")
                return False
        
        def verify_click_account_information(self):
            try:
                account_back = self.wait_for_element(
                    self.return_button
                )
                return account_back is not None
            except Exception as e:
                logger.error(f"异常信息{e}")
                return False
                raise
