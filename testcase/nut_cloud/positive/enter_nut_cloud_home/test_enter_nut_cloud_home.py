import logging
from collections import Counter

import allure
import pytest

from pages.nut_cloud_page.home_page import HomePage
from utils.test_data_loader import load_test_data

new_folder_coordinates_data = load_test_data("new_folder_version_coordinates.json")
list_pattern_coordinates_data = load_test_data("list_pattern_coordinates.json")
batch_management_coordinates_data = load_test_data("batch_management_coordinates.json")
sort_coordinates_data = load_test_data("sort_coordinates.json")
account_coordinates = load_test_data("account_coordinates.json")
logger = logging.getLogger(__name__)
folder_test_data = load_test_data("click_folder_test.json")
folder_name_enter_data = load_test_data("enter_home_folder_name.json")
folder1 = ["我的坚果云"]
folder2 = ["多pdf"]


@pytest.mark.run(order=9)
@allure.epic("坚果云网盘文件主页测试")
@allure.feature("文件主页")
class TestEnterNutCloudHome:
    
    @allure.story("用户点击返回按钮")
    @allure.title("用户验证是否退回网盘主页")
    @pytest.mark.parametrize("enter_folder_page", [(folder1, folder2)], indirect=True)
    def test_click_return_button(self, click_nut_cloud, enter_nut_cloud_home, enter_folder_page):
        enter_nut_cloud_home.set_skip_default_cleanup()
        enter_folder_page.set_skip_default_cleanup()
        
        def enter_nut_cloud():
            home_page = HomePage(enter_nut_cloud_home.driver)
            home_page.click_cloud()
        
        enter_nut_cloud_home.register_cleanup(enter_nut_cloud)  # 针对 enter_nut_cloud_home
        with allure.step("点击首页返回按钮"):
            result = enter_nut_cloud_home.click_return_button()
            assert result.verify_return_cloud_home_page() is True, f"网盘文件主页返回到网盘主页失败"
    
    @allure.story("用户点击搜索按钮")
    @allure.title("用户验证是否进入搜索页面")
    def test_click_search_button(self, enter_nut_cloud_home):
        with allure.step("点击搜索按钮"):
            document_list = enter_nut_cloud_home.get_all_document_names()
            result = enter_nut_cloud_home.click_search_button()
            search_document_list = result.get_all_search_document_names()
            assert Counter(document_list) == Counter(search_document_list), f"点击搜索按钮后文件列表未正常显示"
            assert result.verify_enter_search_page() == '请输入搜索文件名', f"进入搜索页失败"
    
    @allure.story("用户点击传输列表按钮")
    @allure.title("用户验证是否进入传输列表")
    def test_click_transmission_list(self, enter_nut_cloud_home):
        with allure.step("点击传输按钮"):
            result = enter_nut_cloud_home.click_transmission_button()
            assert result.verify_click_enter_transmission_list() == "传输列表", f"进入传输列表失败"
    
    @allure.story("用户点击刷新按钮")
    @allure.title("用户验证弹出刷新提示")
    def test_click_refresh_button(self, enter_nut_cloud_home):
        enter_nut_cloud_home.set_skip_default_cleanup()
        with allure.step("点击刷新"):
            enter_nut_cloud_home.click_refresh_button()
    
    @allure.story("用户点击更多按钮")
    @allure.title("验证点击更多按钮后出现弹窗")
    def test_click_more_button(self, enter_nut_cloud_home):
        with allure.step("点击更多"):
            enter_nut_cloud_home.click_more_button()
    
    @allure.story("用户点击新建文件夹")
    @allure.title("验证点击新建文件夹后是否出现新建弹窗")
    def test_click_new_folder_button(self, more_pop_window_page, enter_nut_cloud_home):
        enter_nut_cloud_home.set_skip_default_cleanup()
        
        def click_return():
            more_pop_window_page.navigate_back(2)
        
        more_pop_window_page.register_cleanup(click_return)
        with allure.step("点击新建文件夹"):
            more_pop_window_page.click_specify_coordinates(new_folder_coordinates_data)
            assert enter_nut_cloud_home.get_new_file_text() == "新建文件夹", f"点击更多按钮失败"
    
    @allure.story("用户点击列表模式")
    @allure.title("验证点击列表模式后文件显示方式变为列表")
    def test_switch_list_mode(self, more_pop_window_page, enter_nut_cloud_home):
        enter_nut_cloud_home.set_skip_default_cleanup()
        
        with allure.step("点击列表模式"):
            result = more_pop_window_page.click_specify_coordinates(list_pattern_coordinates_data)
            assert result.verify_switch_list_mode_success(), f"切换列表模式失败"
    
    @allure.story("用户点击视图模式")
    @allure.title("验证点击视图模式后文件显示方式变为视图")
    def test_switch_view_mode(self, more_pop_window_page, enter_nut_cloud_home):
        enter_nut_cloud_home.set_skip_default_cleanup()
        with allure.step("点击视图模式"):
            result = more_pop_window_page.click_specify_coordinates(list_pattern_coordinates_data)
            assert result.verify_switch_view_mode_success(), f"切换列表模式失败"
    
    @allure.story("用户点击批量管理")
    @allure.title("验证点击批量管理后出现对应功能窗口")
    def test_click_batch_management(self, more_pop_window_page):
        def return_file_home():
            more_pop_window_page.click_batch_management_return()
        
        more_pop_window_page.register_cleanup(return_file_home)
        with allure.step("点击批量管理"):
            result = more_pop_window_page.click_specify_coordinates(batch_management_coordinates_data)
            assert result.verify_click_batch_management_success(), f"点击批量管理失败"
    
    @allure.story("用户点击排序")
    @allure.title("验证排序弹窗正确弹出")
    def test_click_sort(self, more_pop_window_page):
        def click_return():
            more_pop_window_page.navigate_back(1)
        
        more_pop_window_page.register_cleanup(click_return)
        with allure.step("点击排序"):
            result = more_pop_window_page.click_specify_coordinates(sort_coordinates_data)
            assert result.verify_click_sort_success() == '排序', f"点击排序按钮失败"
    
    @allure.story("用户点击账户信息")
    @allure.title("验证进入账户信息界面")
    def test_click_account_Information(self, more_pop_window_page, enter_nut_cloud_home):
        enter_nut_cloud_home.set_skip_default_cleanup()
        
        def enter_nut_cloud():
            more_pop_window_page.navigate_back(1)
            home_page = HomePage(enter_nut_cloud_home.driver)
            home_page.click_cloud()
        
        enter_nut_cloud_home.register_cleanup(enter_nut_cloud)
        with allure.step("点击账户信息"):
            result = more_pop_window_page.click_specify_coordinates(account_coordinates)
            assert result.verify_click_account_information(), f"点击账户信息失败"
    
    @allure.story("点击全部选择框")
    @allure.title("验证所有文件夹被选中")
    def test_select_all_files(self, enter_nut_cloud_home):
        enter_nut_cloud_home.set_skip_default_cleanup()
        
        def cancel_select_files():
            enter_nut_cloud_home.navigate_back(1)
            home_page = HomePage(enter_nut_cloud_home.driver)
            home_page.click_cloud()
        
        enter_nut_cloud_home.register_cleanup(cancel_select_files)
        
        with allure.step("选中全部选择框"):
            result = enter_nut_cloud_home.select_all_current_page()
            assert result.verify_all_selected_successfully(), f"验证元素全部选中失败请重试"
    
    @allure.story("根据文件名称点击复选框")
    @allure.title("验证是否选中以及选中个数是否正确")
    @pytest.mark.parametrize("folder_data", folder_test_data, ids=[case["test_name"] for case in folder_test_data])
    def test_select_all_files1(self, enter_nut_cloud_home, folder_data):
        enter_nut_cloud_home.set_skip_default_cleanup()
        
        def cancel_select_files():
            enter_nut_cloud_home.navigate_back(1)
            home_page = HomePage(enter_nut_cloud_home.driver)
            home_page.click_cloud()
        
        enter_nut_cloud_home.register_cleanup(cancel_select_files)
        result = enter_nut_cloud_home
        filenames = folder_data["filenames"]
        with allure.step(f"根据{filenames}文件名称进行选择复选框"):
            result.click_checkbox_filename(filenames)
        with allure.step(f"验证当前文件名为：{filenames}是否选择复选框成功"):
            assert result.verify_checkbox_click_status(filenames, 'true')
        with allure.step(f"验证选择当前文件个数是否正确"):
            assert result.get_selected_number() == len(
                filenames), f"文件点击选择个数失败。获取数量：{result.get_selected_number()},实际数量：{len(filenames)}"
    
    @allure.story("用户点击下一页")
    @allure.title("验证是否翻页")
    def test_click_next_page(self, enter_nut_cloud_home):
        result = enter_nut_cloud_home
        result.set_skip_default_cleanup()
        expected_page_count = result.click_next_page()
        current_page, all_pages = result.get_page_number()
        assert current_page == expected_page_count, f"点击下一页失败，当前页数：{current_page}，预期页数：{expected_page_count}"
    
    @allure.story("用户点击上一页")
    @allure.title("验证是否翻页")
    def test_click_pre_page(self, enter_nut_cloud_home):
        result = enter_nut_cloud_home
        result.set_skip_default_cleanup()
        current_page, all_pages = result.get_page_number()
        expected_page_count = result.click_pre_page()
        current_page, all_pages = result.get_page_number()
        assert current_page == expected_page_count, f"点击下一页失败，当前页数：{current_page}，预期页数：{expected_page_count}"
    
    @allure.story("用户选择文件后翻页")
    @allure.title("验证文件选择状态消失")
    def test_click_on_the_folder_to_flip_pages(self, enter_nut_cloud_home):
        result = enter_nut_cloud_home
        result.set_skip_default_cleanup()
        
        def cancel_select_files():
            result.navigate_back(1)
            home_page = HomePage(result.driver)
            home_page.click_cloud()
        
        result.register_cleanup(cancel_select_files)
        
        filenames = ['我的坚果云']
        # 点击文件复选框
        result.click_checkbox_filename(filenames)
        verify_element_check_success = result.verify_checkbox_click_status(filenames, 'true')
        assert verify_element_check_success, f"点击选择文件夹：{filenames}失败"
        result.click_next_page()
        result.click_pre_page()
        verify_element_check_failure = result.verify_checkbox_click_status(filenames, 'false')
        assert verify_element_check_failure, f"点击选择文件夹：{filenames}失败"
    
    @allure.story("用户点击文件夹")
    @pytest.mark.parametrize("folder_name_data", folder_name_enter_data,
                             ids=[data["test_name"] for data in folder_name_enter_data])
    def test_enter_nut_folder(self, enter_nut_cloud_home, folder_name_data):
        with allure.step("点击进入文件夹"):
            result = enter_nut_cloud_home
            filenames = folder_name_data["filenames"]
            allure.title(f"验证是否进入{filenames}文件夹")
            # 点击文件复选框
            result.click_folder_filename(filenames)
            
            # 验证点击是否成功
            get_element_check = result.verify_enter_nut_folder() == filenames[0]
            assert get_element_check, f"进入坚果云文件夹失败"
