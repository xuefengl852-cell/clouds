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
    
    def get_return_text(self):
        try:
            return_text = self.get_element_attribute(
                self.tv_drive,
                "text"
            )
            folder_text = return_text.replace("/", 1)
            return folder_text
        except Exception as e:
            logger.error(f"获取当前返回文本失败：{e}")
    
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
    
    def get_selected_number(self):
        try:
            selected_number = self.get_element_attribute(
                self.select_ed,
                "text"
            )
            if selected_number and "已选择" in selected_number:
                number_str = selected_number.replace("已选择", "")
                number = int(number_str)
        except Exception as e:
            logger.error(f"获取选择数量失败：{e}")
        return number
    
    def get_page_number(self):
        page_text = self.get_page_number_text()
        current_page, all_pages = map(int, page_text.split('/'))
        return current_page, all_pages
    
    def click_next_page(self):
        """点击下一页"""
        current_page, all_pages = self.get_page_number()
        if current_page < all_pages:
            try:
                self.click(self.next_page)
                logger.info(f"翻页成功，当前页变为: {current_page + 1}")
                return current_page + 1
            except Exception as e:
                logger.error(f"翻页过程中出错: {e}")
        else:
            logger.warning("已是最后一页，无法继续翻页")
    
    def click_pre_page(self):
        """点击上一页"""
        current_page, all_pages = self.get_page_number()
        if current_page > 1:
            try:
                self.click(self.pre_page)
                logger.info(f"向前翻页成功")
                return current_page - 1
            except Exception as e:
                logger.error(f"翻页过程中出错: {e}")
        else:
            logger.warning("无法向前翻页")
    
    def click_checkbox_filename(self, filenames):
        """
        通过文件名称进行点击文件夹复选框
        :param filenames: 文件名称列表
        :return: T/F
        """
        current_page, all_pages = self.get_page_number()
        
        # 遍历所有页面
        while current_page < all_pages:
            click_status = self.click_based_on_the_file_name(
                self.root_layout,
                self.file_grid_tv_id,
                self.jan_grid_chb,
                filenames
            )
            if click_status:
                logger.info(f"在：{current_page}页，选择：{filenames}复选框成功")
                break
            else:
                logger.warning(f"在：{current_page}页，选择：{filenames}复选框失败，进行翻页")
                self.click_next_page()
        return click_status
    
    def long_press_the_folder_by_name(self, filename):
        """根据名称长按文件夹"""
        try:
            self.long_press_based_on_the_file_name(
                self.root_layout,
                self.file_grid_tv_id,
                self.jan_grid_tv,
                filename
            )
        except Exception as e:
            logger.error(f"长安文件夹失败：{e}")
        return self
    
    def verify_long_folder_success(self):
        try:
            image_view = self.wait_for_element(
                self.cover_file_tv
            )
            return image_view is not None
        except Exception as e:
            logger.error(f"验证文件夹元素存在失败：{e}")
            return False
    
    def get_file_suffix(self):
        try:
            file_suffix_text = self.get_element_attribute(
                self.ja_document_name_iv,
                "text"
            )
            logger.info(f"文件图标文本为：{file_suffix_text}")
            return file_suffix_text
        except Exception as e:
            logger.error(f"获取文件图标文本失败：{e}")
    
    def get_file_title(self):
        try:
            file_title = self.get_element_attribute(
                self.title_file_tv,
                "text"
            )
            filename_suffix_text = file_title.rsplit(':', 1)
            logger.info(f"文件标题文本为：{file_title}")
            return filename_suffix_text[1]
        except Exception as e:
            logger.error(f"获取文件标题文本失败：{e}")
    
    def get_file_information(self):
        try:
            file_title = self.get_element_attribute(
                self.type_file_tv,
                "text"
            )
            filename_suffix_text = file_title.rsplit(':', 1).lower()
            logger.info(f"文件标题文本为：{file_title}")
            return filename_suffix_text[1]
        except Exception as e:
            logger.error(f"获取文件标题文本失败：{e}")
    
    def get_file_size(self):
        try:
            file_size = self.wait_for_element(
                self.size_file_tv
            )
            return file_size is not None
        except Exception as e:
            logger.error(f"获取文件大小失败：{e}")
            return False
    
    def get_file_time(self):
        try:
            file_time = self.wait_for_element(
                self.time_file_tv
            )
            return file_time is not None
        except Exception as e:
            logger.error(f"获取文件时间失败：{e}")
            return False
    
    def get_file_name(self):
        try:
            file_title = self.get_element_attribute(
                self.name_file_tv,
                "text"
            )
            logger.info(f"文件名称文本为：{file_title}")
            return file_title
        except Exception as e:
            logger.error(f"获取文件标题文本失败：{e}")
    
    def get_item_name(self):
        try:
            item_name_tv = self.wait_for_element(
                self.item_name_tv
            )
            return item_name_tv is not None
        except Exception as e:
            logger.error(f"获取工具栏失败：{e}")
            return False
    
    def verify_long_action_bar_success(self):
        try:
            detail_grid_view = self.wait_for_element(
                self.detail_grid_view
            )
            return detail_grid_view is not None
        except Exception as e:
            logger.error(f"验证文件夹元素存在失败：{e}")
            return False
    
    def enter_file_page(self, filenames):
        try:
            success = False
            if not success:
                self.click_based_on_the_file_name(
                    self.root_layout,
                    self.file_grid_tv_id,
                    self.jan_grid_tv,
                    filenames
                )
                success = True
            else:
                logger.error(f"点击进入：{filenames}文件夹失败")
        except Exception as e:
            logger.error(f"进入文件夹失败：{e}")
        return success
    
    def get_folder_detail_page_name(self):
        try:
            name_text = self.get_element_attribute(
                self.name_file_tv,
                "text"
            )
            return name_text
        except Exception as e:
            logger.error(f"获取详情页文件夹名称失败：{e}")
    
    def click_folder_filename(self, filenames):
        """
        通过文件名称进行点击文件夹
        :param filenames: 文件名称列表
        :return: 点击文件个数
        """
        current_page, all_pages = self.get_page_number()
        while current_page < all_pages:
            click_status = self.click_based_on_the_file_name(
                self.root_layout,
                self.file_grid_tv_id,
                self.jan_grid_tv,
                filenames
            )
            if click_status:
                logger.info(f"在第{current_page}页，点击进入：{filenames}文件夹成功")
                break
            else:
                logger.warning(f"在第{current_page}页，未找到{filenames}文件夹，进行下一页查找")
                self.click_next_page()
        return click_status
    
    def verify_enter_nut_folder(self):
        try:
            element_text = self.get_element_attribute(
                self.tv_drive,
                "text"
            )
            return element_text
        except Exception as e:
            logger.error(f"获取当前页文件夹文本失败：{e}")
            raise
    
    def verify_checkbox_click_status(self, filenames, status_text):
        """
        验证复选框是否点击成功
        :param status_text: 预期状态文本
        :param filenames: 文件名列表
        :return: 布尔值，所有文件都选中返回True，否则返回False
        """
        try:
            # 获取状态字典
            status_dict = self.get_locator_checked_status(
                self.root_layout,
                self.file_grid_tv_id,
                self.jan_grid_chb,
                filenames
            )
            # 调试：打印返回的数据类型和内容
            logger.debug(f"返回的数据内容: {status_dict}")
            # 检查文件是否被选中
            for filenames, status in status_dict.items():
                # 判断文件选择状态
                if status == status_text:
                    logger.info(f"文件：{filenames}状态为：{status}，预期为：{status_text} ")
                    return True
                else:
                    logger.error(f"文件：{filenames}状态为：{status}，预期为：{status_text} ")
                    return False
        except Exception as e:
            logger.error(f"验证复选框点击状态失败: {e}")
            return False
    
    def get_page_number_text(self):
        try:
            page_number_text = self.get_element_attribute(
                self.page_tv,
                "text"
            )
            logger.info(f"当前页面页码为：{page_number_text}")
            return page_number_text
        except Exception as e:
            logger.error(f"获取页码失败{e}")
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
