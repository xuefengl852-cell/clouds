import allure
import pytest

from pages.nut_cloud_page.search_page import SearchPage
from utils.test_data_loader import load_test_data

search_check_home_page_data = load_test_data("download_large_memory_files_data.json")
copy_page_enter_folder = load_test_data("copy_page_enter_folder.json")


@pytest.mark.parametrize(
    # 声明3个参数（与 fixture 一一对应）
    "check_test_data, folder_name_first, enter_folder_second",
    # 修复1：参数值推导式（按索引一一对应，取较短数据长度避免越界）
    [
        (
              # 1. 搜索文件名（来自第一个 JSON，直接取字符串）
              search_check_home_page_data[i]["search_name"],
              # 2. 第一层文件夹名（JSON 中是列表，取第一个元素转字符串）
              copy_page_enter_folder[i]["folder_name_first"],
              # 3. 第二层文件夹名（同上，列表转字符串）
              copy_page_enter_folder[i]["enter_folder_second"]
        )
        # 关键修复：取两个 JSON 中较短的长度，避免索引越界
        for i in range(min(len(search_check_home_page_data), len(copy_page_enter_folder)))
    ],
    # 修复2：ids 用 copy_page_enter_folder 的 test_name（更贴合用例语义，且索引安全）
    ids=[
        f"{copy_page_enter_folder[i]['test_name']}_search:{search_check_home_page_data[i]['search_name']}"
        for i in range(min(len(search_check_home_page_data), len(copy_page_enter_folder)))
    ],
    # 修复3：indirect 加入另外两个 fixture（否则 fixture 拿不到 request.param）
    indirect=["check_test_data", "folder_name_first", "enter_folder_second"]
)
@allure.story("复制页面新建文件夹")
@pytest.mark.run(order=27)
class TestCopyPageNewFolder:
    
    @allure.title("新建文件夹")
    def test_new_folder(self, click_search_copy_btn, folder_name_first, enter_folder_second, check_test_data):
        result = click_search_copy_btn
        
        def click_cancel_btn():
            result.click_copy_cancel_button()
        
        result.register_cleanup(click_cancel_btn)
        
        with allure.step("点击新建文件夹"):
            result.click_new_folder()
        with allure.step("验证新建文件夹窗口是否存在"):
            assert result.verify_new_folder_windows()
    
    @allure.title("取消新建文件夹")
    def test_cancel_new_folder(self, click_search_copy_new_folder_btn, app_driver):
        result = click_search_copy_new_folder_btn
        
        def click_cancel_btn():
            search_page = SearchPage(app_driver)
            result.click_cancel_copy_btn()
            search_page.click_cancel_but()
            search_page.click_search_return()
        
        result.register_cleanup(click_cancel_btn)
        
        with allure.step("点击取消按钮"):
            result.click_copy_cancel_button()
