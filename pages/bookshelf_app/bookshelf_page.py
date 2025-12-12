import logging

from base.base_page import BasePage
from locators.bookshelf_page_locators import BookshelfPageLocators
from utils.loactor_validator import LocatorValidator

logger = logging.getLogger(__name__)
locator_validator = LocatorValidator()
bookshelf_locators = BookshelfPageLocators()


class BookshelfPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        # 验证必需的定位器配置
        locator_validator.validate(self)
    
    @property
    def layout(self):
        return self.get_locator(bookshelf_locators.PAGE_SECTION, bookshelf_locators.LAYOUT)
    
    @property
    def image_view_1(self):
        return self.get_locator(bookshelf_locators.PAGE_SECTION, bookshelf_locators.IMAGE_VIEW_1)
    
    @property
    def tv_book_title(self):
        return self.get_locator(bookshelf_locators.PAGE_SECTION, bookshelf_locators.TV_BOOK_TITLE)
    
    @property
    def rl_title_folder(self):
        return self.get_locator(bookshelf_locators.PAGE_SECTION, bookshelf_locators.RL_TITLE_FOLDER)
    
    @property
    def iv_more(self):
        return self.get_locator(bookshelf_locators.PAGE_SECTION, bookshelf_locators.IV_MORE)
    
    @property
    def tv_batch(self):
        return self.get_locator(bookshelf_locators.PAGE_SECTION, bookshelf_locators.TV_BATCH)
    
    @property
    def ll_select(self):
        return self.get_locator(bookshelf_locators.PAGE_SECTION, bookshelf_locators.LL_SELECT)
    
    @property
    def ll_upload_net(self):
        return self.get_locator(bookshelf_locators.PAGE_SECTION, bookshelf_locators.LL_UPLOAD_NET)
    
    @property
    def iv_manage_cancel(self):
        return self.get_locator(bookshelf_locators.PAGE_SECTION, bookshelf_locators.IV_MANAGE_CANCEL)
    
    @property
    def next_btn(self):
        return self.get_locator(bookshelf_locators.PAGE_SECTION, bookshelf_locators.NEXT_BTN)
    
    @property
    def previous_btn(self):
        return self.get_locator(bookshelf_locators.PAGE_SECTION, bookshelf_locators.PREVIOUS_BTN)
    
    @property
    def progress_tv(self):
        return self.get_locator(bookshelf_locators.PAGE_SECTION, bookshelf_locators.PROGRESS_TV)
    
    @property
    def tv_folder(self):
        return self.get_locator(bookshelf_locators.PAGE_SECTION, bookshelf_locators.TV_FOLDER)
    
    @property
    def tv_group_name(self):
        return self.get_locator(bookshelf_locators.PAGE_SECTION, bookshelf_locators.TV_GROUP_NAME)
    
    @property
    def ll_delete(self):
        return self.get_locator(bookshelf_locators.PAGE_SECTION, bookshelf_locators.LL_DELETE)
    
    @property
    def cb_check(self):
        return self.get_locator(bookshelf_locators.PAGE_SECTION, bookshelf_locators.CB_CHECK)
    
    @property
    def enter_btn(self):
        return self.get_locator(bookshelf_locators.PAGE_SECTION, bookshelf_locators.ENTER_BTN)
    
    def get_bookshelf_folder_name(self):
        try:
            folder_list = self.get_all_folder_texts(
                bookshelf_locators.PAGE_SECTION,
                bookshelf_locators.TV_GROUP_NAME
            )
            logger.info(f"当前页面所有文件夹为：{folder_list}")
            return folder_list
        except Exception as e:
            logger.error(f"获取当前页面文件夹失败：{e}")
            raise e
    
    def verify_nut_store_exist(self, target_folder_name):
        folder_list_name = self.get_bookshelf_folder_name()
        try:
            if target_folder_name in folder_list_name:
                logger.info(f"目标文件夹名称：{target_folder_name}存在")
                return True
            else:
                logger.error(f"目标文件夹未出现在当前目录下")
                return False
        except Exception as e:
            raise False
            raise e
    
    def get_bookshelf_number_text(self):
        """获取书架当前页/总页"""
        try:
            page_text = self.get_element_attribute(
                self.progress_tv,
                "text"
            )
            
            current_page, all_pages = map(int, page_text.split('/'))
            return current_page, all_pages
        except Exception as e:
            logger.error(f"获取书架页码失败{e}")
            raise
    
    def click_bookshelf_folder(self, folder_name):
        """根据文件名点击书架文件夹"""
        current_page, all_pages = self.get_bookshelf_number_text()
        try:
            self.click_based_on_the_file_name(
                self.layout,
                self.tv_group_name,
                self.layout,
                folder_name,
                all_pages,
                current_page,
                self.next_btn
            )
            logger.info(f"点击：{folder_name}文件夹成功")
        except Exception as e:
            logger.error(f"点击{folder_name}文件夹失败")
            raise e
    
    def get_bookshelf_current_folder_name(self):
        """获取文件夹名称"""
        try:
            folder_name = self.get_element_attribute(
                self.tv_folder,
                "text"
            )
            logger.info(f"书架当前文件夹名称为:{folder_name}")
            return folder_name
        except Exception as e:
            logger.error(f"获取书架当前文件名称失败")
            raise e
    
    def get_select_all_file_name(self):
        """获取当前文件夹内所有文件名称"""
        try:
            file_list = self.get_all_folder_texts(
                bookshelf_locators.PAGE_SECTION,
                bookshelf_locators.TV_BOOK_TITLE
            )
            logger.info(f"当前页所有文件为:{file_list}")
            return file_list
        except Exception as e:
            logger.error(f"获取当前页文件名称失败")
            raise e
    
    def click_bookshelf_more_btn(self):
        """点击更多按钮"""
        try:
            self.click(
                self.iv_more
            )
            logger.info(f"点击书架更多按钮成功")
        except Exception as e:
            logger.error(f"点击书架更多按钮失败")
            raise e
        return self
    
    def click_bookshelf_batch_management_btn(self):
        """点击批量管理按钮"""
        try:
            self.click(
                self.tv_batch
            )
            logger.info(f"点击书架批量管理成功")
        except Exception as e:
            logger.error(f"点击书架批量管理失败")
            raise e
        return self
    
    def click_bookshelf_select_all_btn(self):
        """点击全选按钮"""
        try:
            self.click(
                self.ll_select
            )
            logger.info(f"点击书架全选成功")
        except Exception as e:
            logger.error(f"点击书架全选失败")
            raise e
        return self
    
    def click_bookshelf_remove_btn(self):
        """点击移出按钮"""
        try:
            self.click(
                self.ll_delete
            )
            logger.info(f"点击书架移出成功")
        except Exception as e:
            logger.error(f"点击书架移出失败")
            raise e
        return self
    
    def click_bookshelf_delete_load_btn(self):
        """点击本地源文件按钮"""
        try:
            self.click(
                self.cb_check
            )
            logger.info(f"点击书架本地源文件成功")
        except Exception as e:
            logger.error(f"点击书架本地源文件失败")
            raise e
        return self
    
    def click_bookshelf_sure_btn(self):
        """点击确定按钮"""
        try:
            self.click(
                self.enter_btn
            )
            logger.info(f"点击书架确定成功")
        except Exception as e:
            logger.error(f"点击书架确定失败")
            raise e
        return self
    
    def click_return_bookshelf_home_btn(self):
        """点击书架返回按钮"""
        try:
            self.click(
                self.rl_title_folder
            )
            logger.info(f"点击返回书架主页成功")
        except Exception as e:
            logger.error(f"点击返回书架主页失败")
            raise e
        return self
