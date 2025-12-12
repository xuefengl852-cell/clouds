import allure
import pytest

from utils.test_data_loader import load_test_data

search_check_home_page_data = load_test_data("test_download_single_file_data.json")

nut_store_list = ['NutStore']


@pytest.mark.run(order=22)
@allure.story("单个文件下载")
class TestDownLoadMultipleFile:
    @pytest.mark.parametrize(
        # 声明需要传递的参数：input_name（给input_name fixture）和check_test_data（给check_test_data fixture）
        "check_test_data",
        # 参数值：按顺序对应input_name和check_test_data
        [
            (
                  search_check_home_page_data[i]["search_name"]  # check_test_data的值
            )
            for i in range(len(search_check_home_page_data))
        ],
        # 用例标识（可选，增强报告可读性）
        ids=[
            f"{search_check_home_page_data[i]['test_name']}_check"
            for i in range(len(search_check_home_page_data))
        ],
        # 指定参数传递给对应的fixture
        indirect=["check_test_data"]
    )
    @allure.title("钩选单个文件点击下载")
    def test_single_file_download(self, search_check_box_file, app_driver, check_test_data, app_switcher,
                                  bookshelf_home):
        result, document_home_page = search_check_box_file
        
        def enter_search_page():
            bookshelf_home.click_bookshelf_more_btn() \
                .click_bookshelf_batch_management_btn() \
                .click_bookshelf_select_all_btn() \
                .click_bookshelf_remove_btn() \
                .click_bookshelf_delete_load_btn() \
                .click_bookshelf_sure_btn() \
                .click_return_bookshelf_home_btn()
            app_switcher.switch_hv_drive_app()
            result.restore_drive_application_status(app_driver)
            result.check_box_download_file(check_test_data)
            result.click_download_list_delete_btn()
            result.check_box_delete_load_file()
            result.click_confirm_delete()
            result.click_return_home_page()
            result.click_search_document_but()
        
        result.register_cleanup(enter_search_page)
        
        with allure.step("点击下载"):
            result.click_download_btn()
        with allure.step("进入传输列表"):
            result.navigate_back(1)
            result.click_transmission_list_btn()
        progress_dict = result.get_current_download_progress(check_test_data)
        
        for filename in check_test_data:
            assert filename in progress_dict, f"文件名{filename}不在进度字典中，字典key：{list(progress_dict.keys())}"
            actual_progress = progress_dict[filename]
            assert actual_progress == 100, \
                f"文件{filename}下载失败，预期进度100，实际状态：{actual_progress}"
        
        download_file_list = result.get_download_file(check_test_data)
        
        download_number = result.get_download_list_file_number()
        
        with allure.step("验证下载数量是否正确"):
            assert len(download_number) == len(
                check_test_data), f"下载数量错误，勾选数量：{len(download_number)}，文件数量：{len(check_test_data)}"
        app_switcher.switch_bookshelf_app()
        assert bookshelf_home.verify_nut_store_exist(nut_store_list[0]), f"目标文件夹：{nut_store_list[0]}未出现在书架"
        bookshelf_home.click_bookshelf_folder(nut_store_list)
        current_folder_name = bookshelf_home.get_bookshelf_current_folder_name()
        assert current_folder_name == nut_store_list[0], f"进入坚果云文件夹失败，当前文件夹为：{current_folder_name}"
        file_name_list = bookshelf_home.get_select_all_file_name()
        assert set(download_file_list) == set(
            file_name_list), f"书架中文件{file_name_list}与下载列表文件{download_number}不一致"
