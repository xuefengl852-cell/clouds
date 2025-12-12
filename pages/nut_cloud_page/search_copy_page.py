import logging

from base.base_page import BasePage
from locators.search_copy_page_locators import SearchCopyPageLocators
from pages.cloud_sort_page import locator_validator

logger = logging.getLogger(__name__)
locators = SearchCopyPageLocators()


class SearchCopyPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # 验证必需的定位器配置
        locator_validator.validate(self)
    
    @property
    def new_folder(self):
        return self.get_locator(locators.PAGE_SECTION, locators.NEW_FOLDER)
    
    @property
    def tv_folder_name(self):
        return self.get_locator(locators.PAGE_SECTION, locators.TV_FOLDER_NAME)
    
    @property
    def rb_select(self):
        return self.get_locator(locators.PAGE_SECTION, locators.RB_SELECT)
    
    @property
    def page_left(self):
        return self.get_locator(locators.PAGE_SECTION, locators.PAGE_LEFT)
    
    @property
    def page_right(self):
        return self.get_locator(locators.PAGE_SECTION, locators.PAGE_RIGHT)
    
    @property
    def root_item_layout(self):
        return self.get_locator(locators.PAGE_SECTION, locators.ROOT_ITEM_LAYOUT)
    
    @property
    def page_tv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.PAGE_TV)
    
    @property
    def dialog_cancel(self):
        return self.get_locator(locators.PAGE_SECTION, locators.DIALOG_CANCEL)
    
    @property
    def dialog_sure(self):
        return self.get_locator(locators.PAGE_SECTION, locators.DIALOG_SURE)
    
    @property
    def bt_enter(self):
        return self.get_locator(locators.PAGE_SECTION, locators.BT_ENTER)
    
    @property
    def tv_rack_nimble(self):
        return self.get_locator(locators.PAGE_SECTION, locators.TV_RACK_NIMBLE)
    
    @property
    def jan_new_file_tv(self):
        return self.get_locator(locators.PAGE_SECTION, locators.JAN_NEW_FILE_TV)
    
    @property
    def nick_name_cancel(self):
        return self.get_locator(locators.PAGE_SECTION, locators.NICK_NAME_CANCEL)
    
    def click_new_folder(self):
        """复制窗口点击新建文件夹"""
        try:
            self.click(self.new_folder)
            logger.info(f"点击新建文件夹成功")
        except Exception as e:
            logger.error(f"点击新建文件夹失败")
            raise e
    
    def verify_new_folder_windows(self):
        """验证新建文件夹窗口存在"""
        try:
            new_folder = self.wait_for_element(
                self.jan_new_file_tv
            )
            logger.info(f"新建文件夹窗口存在")
            return new_folder is not None
        except Exception as e:
            logger.error(f"新建文件夹窗口不存在")
            raise e
    
    def click_copy_cancel_button(self):
        """在新建文件夹窗口点击取消按钮"""
        try:
            self.click(self.nick_name_cancel)
            logger.info(f"点击取消新建文件夹成功")
        except Exception as e:
            logger.error("点击取消新建文件夹失败")
            raise e
    
    def get_copy_page_number_text(self):
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
    
    def enter_copy_page_folder_name(self, folder_name):
        """根据文件夹名称勾选文件"""
        try:
            current_page, all_pages = self.get_copy_page_number_text()
            self.click_based_on_the_file_name(
                self.root_item_layout,
                self.tv_folder_name,
                self.root_item_layout,
                folder_name,
                current_page,
                all_pages,
                self.page_right
            )
            logger.info(f"搜索-复制页面，{folder_name}文件夹进入成功")
        except Exception as e:
            logger.error(f"搜索-复制页面，{folder_name}文件夹进入失败")
            raise e
    
    def check_copy_page_folder_name(self, folder_name):
        """根据文件夹名称勾选文件"""
        try:
            current_page, all_pages = self.get_copy_page_number_text()
            self.click_based_on_the_file_name(
                self.root_item_layout,
                self.tv_folder_name,
                self.rb_select,
                folder_name,
                current_page,
                all_pages,
                self.page_right
            )
            logger.info(f"勾选复制窗口：{folder_name}。文件夹成功")
        except Exception as e:
            logger.error(f"勾选复制窗口：{folder_name}。文件夹失败")
            raise e
    
    def verify_bookshelf_app_success(self):
        """验证进入书架"""
        try:
            bookshelf_app_element = self.wait_for_element(self.tv_rack_nimble)
            logger.info(f"进入书架成功")
            return bookshelf_app_element is not None
        except Exception as e:
            logger.error(f"进入书架失败")
            raise e
    
    def click_cancel_copy_btn(self):
        
        """点击取消复制按钮"""
        try:
            self.click(
                self.dialog_cancel
            )
            logger.info(f"点击取消复制按钮成功")
        except Exception as e:
            logger.error(f"点击取消复制按钮失败")
            raise e
