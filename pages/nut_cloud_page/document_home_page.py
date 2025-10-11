import logging

from base.base_page import BasePage
from common.device_info import DeviceInfoManager
from locators.document_home_locators import DocumentHomeLocators
from utils.loactor_validator import LocatorValidator

locators = DocumentHomeLocators()
locator_validator = LocatorValidator()
logger = logging.getLogger(__name__)
device_info_manager = DeviceInfoManager()
hardware_version = str(device_info_manager.get_hardware_version())


class DocumentHomePage(BasePage):
    
    def __init__(self, driver):
        super().__init__(driver)
        logger.info(f"进入主页")
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
    def pre_page(self):
        return self.get_locator(locators.PAGE_SECTION, locators.PRE_PAGE)
    
    @property
    def next_page(self):
        return self.get_locator(locators.PAGE_SECTION, locators.NEXT_PAGE)
    
    @property
    def file_item_by_name(self):
        return self.get_locator(locators.PAGE_SECTION, locators.FILE_ITEM_BY_NAME)
    
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
    def jan_new_file_tv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.JAN_NEW_FILE_TV)
    
    def click_return_button(self):
        try:
            self.click(self.return_button)
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
    
    def verify_enter_search_page(self):
        search_text = self.get_element_attribute(
            self.jan_search_et,
            "text"
        )
        return search_text
    
    def get_all_document_names(self):
        """获取主页所有文档名称"""
        return self.get_paginated_data(
            page_indicator_locator=self.page_tv,  # 页码指示器元素
            section=locators.PAGE_SECTION,
            key=locators.FILE_GRID_TV,
            next_button_locator=self.next_page,
            prev_button_locator=self.pre_page
        )
    
    def select_all_current_page(self):
        """
        检查所有元素是否都被选中（主流写法）
        :return: 布尔值，表示是否全部选中
        """
        try:
            self.select_all_click(
                self.jan_grid_chb
            )
        except Exception as e:
            logger.error(f"点击元素失败：{e}")
            raise
        return self
    
    def verify_all_selected_successfully(self):
        """
        验证元素是否被选中
        :return: T/F
        """
        try:
            checked_values = self.get_element_attribute(
                locator=self.jan_grid_chb,
                attribute='checked',
                multiple=True
            )
            if checked_values is None:
                logger.error("无法获取元素选中状态")
                return False
            if not checked_values:
                logger.error(f"未找到任何可验证元素")
                return False
            all_selected = all(value in 'true' for value in checked_values)
            return all_selected
        except Exception as e:
            logger.error(f"验证元素选中状态时发生异常: {e}")
            self.take_screenshot("verify_selection_failed")
            return False
    
    def get_all_search_document_names(self):
        """获取搜索所有文档名称"""
        return self.get_paginated_data(
            page_indicator_locator=self.page_tv,  # 页码指示器元素
            section=locators.PAGE_SECTION,
            key=locators.JAN_LIST_NAME_TV,
            next_button_locator=self.next_page,
            prev_button_locator=self.pre_page
        )
    
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
            try:
                list_mode_logo = self.wait_for_element(
                    self.list_mode
                )
                return list_mode_logo is not None
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
