import logging
import re

from base.base_page import BasePage
from locators.search_page_locators import SearchPageLocators
from utils.loactor_validator import LocatorValidator

logger = logging.getLogger(__name__)
locator_validator = LocatorValidator()
locators = SearchPageLocators()


class SearchPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # 验证必需的定位器配置
        locator_validator.validate(self)
    
    @property
    def search_back(self):
        return self.get_locator(locators.PAGE_SECTION, locators.SEARCH_BACK_IV)
    
    @property
    def search_list_chb(self):
        return self.get_locator(locators.PAGE_SECTION, locators.SEARCH_LIST_CHB)
    
    @property
    def jan_search_et(self):
        return self.get_locator(locators.PAGE_SECTION, locators.JAN_SEARCH_ET)
    
    @property
    def jan_dd_status_tv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.JAN_DD_STATUS_TV)
    
    @property
    def pre_page(self):
        return self.get_locator(locators.PAGE_SECTION, locators.PRE_PAGE)
    
    @property
    def dialog_cancel(self):
        return self.get_locator(locators.PAGE_SECTION, locators.DIALOG_CANCEL)
    
    @property
    def clear_text_iv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.CLEAR_TEXT_IV)
    
    @property
    def bt_search(self):
        return self.get_locator(locators.PAGE_SECTION, locators.BT_SEARCH)
    
    @property
    def copy_dialog_title(self):
        return self.get_locator(locators.PAGE_SECTION, locators.COPY_DIALOG_TITLE)
    
    @property
    def search_btn_tv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.SEARCH_BTN_TV)
    
    @property
    def search_select_ed_tv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.SEARCH_SELECT_ED_TV)
    
    @property
    def root_list_layout(self):
        return self.get_locator(locators.PAGE_SECTION, locators.ROOT_LIST_LAYOUT)
    
    @property
    def page_tv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.PAGE_TV)
    
    @property
    def jan_list_name_tv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.JAN_LIST_NAME_TV)
    
    @property
    def search_btn_tv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.SEARCH_BTN_TV)
    
    @property
    def next_page(self):
        return self.get_locator(locators.PAGE_SECTION, locators.NEXT_PAGE)
    
    @property
    def jan_list_info_tv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.JAN_LIST_INFO_TV)
    
    @property
    def name_file_tv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.NAME_FILE_TV)
    
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
    def ja_document_name_iv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.JA_DOCUMENT_NAME_IV)
    
    @property
    def item_name_tv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.ITEM_NAME_TV)
    
    @property
    def dialog_close(self):
        return self.get_locator(locators.PAGE_SECTION, locators.DIALOG_CLOSE)
    
    @property
    def search_Select_all(self):
        return self.get_locator(locators.PAGE_SECTION, locators.SEARCH_SELECT_ALL)
    
    @property
    def search_copy_tv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.SEARCH_COPY_TV)
    
    @property
    def search_move_tv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.SEARCH_MOVE_TV)
    
    @property
    def search_sec_tv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.SEARCH_SEC_TV)
    
    @property
    def search_delete_tv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.SEARCH_DELETE_TV)
    
    @property
    def bt_download(self):
        return self.get_locator(locators.PAGE_SECTION, locators.BT_DOWNLOAD)
    
    @property
    def dateLayout(self):
        return self.get_locator(locators.PAGE_SECTION, locators.DATE_LAYOUT)
    
    @property
    def janDdInfoTv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.JAN_DD_INFO_TV)
    
    @property
    def janDdTitleNameTv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.JAN_DD_TITLE_NAME_TV)
    
    @property
    def janDdNameIv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.JAN_DD_NAME_IV)
    
    @property
    def download_progress_xpath(self):
        return self.get_locator(locators.PAGE_SECTION, locators.DOWNLOAD_PROF_RESS_XPATH)
    
    def click_search_return(self):
        """在搜索页点击返回按钮"""
        try:
            self.click(self.search_back)
            logger.info(f"点击搜索页返回按钮成功")
        except Exception as e:
            logger.info(f"点击搜索页返回按钮异常：{e}")
            raise e
        return self
    
    def verify_search_button_return_success(self):
        """验证搜索按钮存在"""
        try:
            bt_search_button = self.wait_for_element(
                self.bt_search
            )
            logger.info(f"搜索按钮存在")
            return bt_search_button is not None
        except Exception as e:
            logger.error(f"搜索按钮未找到：{e}")
            return False
    
    def click_search_document_but(self):
        """点击主页搜索按钮"""
        try:
            self.click(self.bt_search)
            logger.info(f"进入搜索页面成功")
        except Exception as e:
            logger.error(f"进入搜索页面异常")
    
    def input_search_name(self, text):
        """在搜索框输入内容"""
        try:
            search_text = self.input_text(
                self.jan_search_et,
                text
            )
            logger.info(f"在搜索框输入：{text}文本成功")
            return search_text
        except Exception as e:
            logger.error(f"输入文本：{text}异常：{e}")
    
    def get_search_text(self):
        """获取输入框内容"""
        try:
            search_input_text = self.get_element_attribute(
                self.jan_search_et,
                "text"
            )
            logger.info(f"已获取输入框文本：{search_input_text}")
            return search_input_text
        except Exception as e:
            logger.error(f"获取文本：{search_input_text}异常：{e}")
    
    def click_clear_button(self):
        """点击输入框回退按钮"""
        try:
            self.click(
                self.clear_text_iv
            )
            logger.info(f"点击回退按钮成功")
        except Exception as e:
            logger.error(f"点击回退按钮失败：{e}")
        return self
    
    def click_search_button(self):
        """点击搜索页面搜索按钮"""
        try:
            self.click(self.search_btn_tv)
            logger.info(f"点击搜索按钮成功")
        except Exception as e:
            logger.error(f"点击搜索按钮失败：{e}")
    
    def verify_search_btn_exist(self):
        """验证搜索按钮存在"""
        try:
            search_btn = self.wait_for_element(
                self.search_btn_tv
            )
            logger.info(f"搜索页面搜索按钮存在")
            return search_btn is not None
        except Exception as e:
            logger.error(f"搜索页面搜索按钮不存在")
            raise e
    
    def get_all_search_document_names(self):
        """获取搜索所有文档名称"""
        return self.get_paginated_data(
            page_indicator_locator=self.page_tv,  # 页码指示器元素
            section=locators.PAGE_SECTION,
            key=locators.JAN_LIST_NAME_TV,
            next_button_locator=self.next_page
        )
    
    def get_page_number_text(self):
        """获取页码当前页、总页数"""
        try:
            page_text = self.get_element_attribute(
                self.page_tv,
                "text"
            )
            
            current_page, all_pages = map(int, page_text.split('/'))
            return current_page, all_pages
        except Exception as e:
            logger.error(f"获取页码失败{e}")
            raise
    
    def click_search_file_name(self, filenames):
        """根据文件名称进行勾选文件"""
        try:
            current_page, all_pages = self.get_page_number_text()
            if isinstance(filenames, str):
                filenames = [filenames]
            logger.info(f"要查找的文件名列表: {filenames}")
            logger.info(f"文件名类型: {type(filenames)}")
            click_status = self.click_based_on_the_file_name(
                self.root_list_layout,
                self.jan_list_name_tv,
                self.search_list_chb,
                filenames,
                current_page,
                all_pages,
                self.next_page
            )
            return click_status
        except Exception as e:
            logger.error(f"根据：{filenames}文件名称点击搜索页文件失败：{e}")
            raise e
    
    def get_locator_select_number(self):
        """获取页面上实际勾选的文件数量（处理元素不存在的情况）"""
        try:
            # 尝试获取元素文本（超时时间可缩短，因为元素要么存在要么不存在）
            text = self.get_element_attribute(
                self.search_select_ed_tv,
                'text',
                condition='visible'  # 只等待“可见”的元素（避免定位到隐藏元素）
            )
            match = re.search(r'\d+', text)
            if text is None or text.strip() == '':
                # 文本为空时，返回 0
                logger.info(f"勾选数量显示元素文本为空，返回 0")
                return 0
            if match:
                number = match.group()
                logger.info(f"已选择文件个数为：{int(number)}")
                return int(number)
        
        except RuntimeError as e:
            # 捕获“元素未找到”的异常（get_element_attribute 会抛 RuntimeError）
            if "获取属性失败" in str(e) and "NoneType" in str(e):
                # 元素不存在，说明勾选数量为 0
                logger.info(f"勾选数量显示元素不存在，返回 0")
                return 0
            else:
                # 其他错误（如文本无法转 int），重新抛出
                logger.error(f"获取勾选数量失败：{str(e)}")
                raise
    
    def verify_cancel_checkbox_number(self, click_file_name, cancel_click_file_name):
        """验证取消勾选"""
        try:
            select_number = len(click_file_name) - len(cancel_click_file_name)
            if select_number >= 0:
                logger.info(f"取消后的数量为：{select_number}")
                return select_number
        except Exception as e:
            logger.error(f"获取取消勾选数量失败")
            raise e
    
    def verify_locator_click_status(self, filenames, status_text):
        """根据文件名称查看元素状态"""
        try:
            status_dict = self.get_locator_checked_status(
                self.root_list_layout,
                self.jan_list_name_tv,
                self.search_list_chb,
                "checked",
                filenames
            )
            logger.info(f"返回的数据内容: {status_dict}")
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
    
    def click_cancel_but(self):
        """点击取消勾选按钮"""
        try:
            self.click(
                self.search_select_ed_tv
            )
            
            logger.info(f"点击取消勾选按钮成功")
        except Exception as e:
            logger.error(f"点击取消勾选按钮失败")
            raise e
    
    def verify_cancel_but_not_success(self):
        """验证取消按钮不存在成功"""
        try:
            cancel_but = self.wait_for_element(
                self.search_select_ed_tv
            )
            logger.info(f"验证取消按钮不存在成功")
            return cancel_but is None
        except Exception as e:
            logger.error(f"取消按钮存在：{e}")
            return False
    
    def long_press_file_name(self, filename):
        """根据名称长按文件夹（修正参数顺序）"""
        try:
            current_page, all_pages = self.get_page_number_text()
            success_count = self.long_press_based_on_the_file_name(
                root_layout_locator=self.root_list_layout,
                file_name_locator=self.jan_list_name_tv,
                target_locator=self.jan_list_name_tv,
                filenames=filename,
                current_page=current_page,
                all_pages=all_pages,
                next_page_locator=self.next_page  # 元组，传入第8个参数
            )
            if success_count == 0:
                raise ValueError(f"未找到文件{filename}或长按未触发")
        except Exception as e:
            logger.error(f"长按文件夹失败：{e}")
            raise e
    
    def get_search_page_file_name(self):
        """获取搜索页面文件名称"""
        try:
            file_name = self.get_element_attribute(
                self.jan_list_name_tv,
                "text"
            )
            return file_name
        except Exception as e:
            logger.error(f"获取搜索页文件名称失败：{e}")
            raise e
    
    def get_past_file_attributes(self):
        """获取搜索页文件属性"""
        try:
            file_attributes = self.get_element_attribute(
                self.jan_list_info_tv,
                "text"
            )
            file_attributes_strip = file_attributes.strip()
            parts = re.split(r'\s+', file_attributes_strip)
            # parts[0], parts[1], parts[2]：时间，类型，大小
            logger.info(f"文件名")
            return parts[0], parts[1], parts[2]
        except Exception as e:
            logger.error(f"获取文件属性失败：{e}")
            raise e
    
    def get_long_file_name(self, filename, current_page, all_pages):
        """根据文件名称获取文件属性（修正时间分割逻辑）"""
        try:
            file_attributes = self.get_file_attributes(
                self.root_list_layout,
                self.jan_list_name_tv,
                self.jan_list_info_tv,
                filename,
                current_page,
                all_pages,
                "text"
            )
            # 确保获取到的属性不为空且是列表
            if not file_attributes or not isinstance(file_attributes, list):
                raise ValueError(f"文件{filename}的属性格式异常：{file_attributes}")
            
            # 取第一个属性字符串并处理空白
            file_attr_str = file_attributes[0].strip()
            # 按空格分割（会得到4个元素：日期、时间、类型、大小）
            parts = re.split(r'\s+', file_attr_str)
            
            # 验证分割结果是否符合预期（必须有4个元素）
            if len(parts) != 4:
                raise ValueError(f"文件{filename}的属性格式错误，分割后元素数量为{len(parts)}：{file_attr_str}")
            
            # 合并日期和时间为完整时间
            full_time = f"{parts[0]} {parts[1]}"  # 如 "2025-11-04 09:20:18"
            file_type = parts[2]  # 如 "pdf"
            file_size = parts[3]  # 如 "1.2MB"
            
            logger.info(f"文件{filename}属性为：时间{full_time}, 类型{file_type}, 大小{file_size}")
            return full_time, file_type, file_size
        
        except Exception as e:
            logger.error(f"获取文件{filename}属性失败：{e}")
            raise e
    
    def get_file_title(self):
        """获取长按后文件标题"""
        try:
            title_text = self.get_element_attribute(
                self.title_file_tv,
                "text"
            )
            parts = title_text.split(':', 1)
            target_content = parts[1].strip()
            logger.info(f"文件标题为：{target_content}")
            return target_content
        except Exception as e:
            logger.info(f"获取文件标题失败：{e}")
            raise e
    
    def get_file_information(self):
        """获取长按后文件信息"""
        try:
            information_text = self.get_element_attribute(
                self.type_file_tv,
                "text"
            )
            parts = information_text.split(':', 1)
            target_content = parts[1].strip()
            logger.info(f"文件信息为：{target_content}")
            return target_content
        except Exception as e:
            logger.info(f"获取文件信息失败：{e}")
            raise e
    
    def get_file_size(self):
        """获取长按后文件大小"""
        try:
            size_text = self.get_element_attribute(
                self.size_file_tv,
                "text"
            )
            parts = size_text.split(':', 1)
            target_content = parts[1].strip()
            logger.info(f"文件大小为：{target_content}")
            return target_content
        except Exception as e:
            logger.info(f"获取文件大小失败：{e}")
            raise e
    
    def get_file_time(self):
        """获取长按后文件时间"""
        try:
            time_text = self.get_element_attribute(
                self.time_file_tv,
                "text"
            )
            parts = time_text.split(':', 1)
            target_content = parts[1].strip()
            logger.info(f"文件时间为：{target_content}")
            return target_content
        except Exception as e:
            logger.info(f"获取文件时间失败：{e}")
            raise e
    
    def get_file_main_name(self):
        """获取长按后文件名称"""
        try:
            name_text = self.get_element_attribute(
                self.name_file_tv,
                "text"
            )
            logger.info(f"文件名称为：{name_text}")
            return name_text
        except Exception as e:
            logger.info(f"获取文件主名称失败：{e}")
            raise e
    
    def get_search_page_name_split(self, file_name):
        """根据名称去掉后缀"""
        try:
            
            parts = file_name.split(".", 1)
            file_name = parts[0].strip()
            logger.info(f"搜素页文件名称（去除后缀）为：{file_name}")
            return file_name
        except Exception as e:
            logger.error(f"获取主页名称（去掉后缀）失败")
            raise e
    
    def click_dialog_close(self):
        """点击关闭长按窗口"""
        try:
            self.click(
                self.dialog_close
            )
            logger.info(f"点击关闭长按窗口成功")
        except Exception as e:
            logger.error(f"点击关闭长按窗口失败：{e}")
            raise e
    
    def verify_file_name_None(self):
        """验证长按关闭后无法定位到名称"""
        try:
            file_name = self.wait_for_element(
                self.name_file_tv
            )
            return file_name is None
        except Exception as e:
            logger.error(f"定位文件名称异常：{e}")
            return False
    
    def click_select_all_but(self):
        """点击搜索页全选按钮"""
        try:
            self.click(self.search_Select_all)
            logger.info(f"搜索页点击全选按钮成功")
        except Exception as e:
            logger.error(f"搜索页点击全选按钮失败：{e}")
            raise e
    
    def click_next_page_but(self):
        """搜索页面点击下一页按钮"""
        try:
            self.click(self.next_page)
            logger.info(f"搜索页面点击下一页成功")
        except Exception as e:
            logger.error(f"搜索页面点击下一页失败")
            raise e
    
    def click_pre_page_but(self):
        """搜索页面点击上一页按钮"""
        try:
            self.click(self.pre_page)
            logger.info(f"搜索页面点击上一页成功")
        except Exception as e:
            logger.error(f"搜索页面点击上一页失败")
            raise e
    
    def get_select_all_element_text(self):
        """获取当前页面所有文档名称"""
        try:
            file_name_text = self.get_all_folder_texts(
                locators.PAGE_SECTION, locators.JAN_LIST_NAME_TV
            )
            logger.info(f"获取到的文本为")
            return file_name_text
        except Exception as e:
            logger.error(f"获取当前页文本失败")
            raise e
    
    def get_select_all_text(self):
        """获取全选按钮文本"""
        try:
            select_text = self.get_element_attribute(
                self.search_Select_all,
                "text"
            )
            logger.info(f"全选/取消全选按钮文本为：{select_text}")
            return select_text
        except Exception as e:
            logger.error(f'获取全选/取消全选文本失败')
            raise e
    
    def click_copy_btn(self):
        """在搜索页点击复制按钮"""
        try:
            self.click(self.search_copy_tv)
            logger.info(f"点击复制按钮成功")
        except Exception as e:
            logger.error(f"点击复制按钮失败")
            raise e
    
    def click_remove_btn(self):
        """搜索页点击移动按钮"""
        try:
            self.click(self.search_move_tv)
            logger.info(f"搜索页点击移动按钮成功")
        except Exception as e:
            logger.info(f"搜索页点击移动按钮失败")
            raise e
    
    def get_dialog_title_text(self):
        """获取弹窗提示文本"""
        try:
            dialog_text = self.get_element_attribute(
                self.copy_dialog_title,
                "text"
            )
            logger.info(f"获取弹窗文本：{dialog_text}，成功")
            return dialog_text
        except Exception as e:
            logger.info(f"获取弹窗文本失败")
            raise e
    
    def click_dialog_cancel_btn(self):
        """点击搜索页面弹窗取消按钮"""
        try:
            self.click(self.dialog_cancel)
            logger.info(f"点击取消按扭成功")
        except Exception as e:
            logger.info(f"点击取消按钮失败")
            raise e
    
    def click_download_btn(self):
        """点击搜索页下载按钮"""
        try:
            self.click(self.search_sec_tv)
            logger.info("点击下载按钮成功")
        except Exception as e:
            logger.error(f"点击下载按钮失败")
            raise e
    
    def click_transmission_list_btn(self):
        """点击输出列表按钮"""
        try:
            self.click(self.bt_download)
            logger.info(f"进入传输列表成功")
        except Exception as e:
            logger.error(f"进入传输列表失败")
            raise e
    
    def verify_download_toast(self):
        """获取当前toast文本内容"""
        try:
            download_toast = self.get_toast_text()
            logger.info(f"当前toast文本为：{download_toast}")
            return download_toast
        except Exception as e:
            logger.error(f"获取当前弹窗文本失败")
            raise e
    
    def check_download_progress(self, filenames):
        downloading = self.wait_for_element(
            locator=self.dateLayout
        )
        download_success = self.wait_for_element(self.jan_dd_status_tv)
        download_dict = self.get_locator_checked_status(
            self.root_list_layout,
            self.janDdTitleNameTv,
            self.jan_dd_status_tv,
            "text",
            filenames
        )
        logger.info(f"************************************{download_dict}")
