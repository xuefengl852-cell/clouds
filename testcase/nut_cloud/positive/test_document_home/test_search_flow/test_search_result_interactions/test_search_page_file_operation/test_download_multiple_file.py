import allure
import pytest

from utils.test_data_loader import load_test_data

search_check_home_page_data = load_test_data("download_large_memory_files_data.json")


@pytest.mark.run(order=23)
@allure.story("多个文件下载")
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
    @allure.title("钩选多个文件点击下载")
    def test_multiple_file_download(self, search_check_box_file, check_test_data):
        result, document_home_page = search_check_box_file
        
        def enter_search_page():
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
        download_number = result.get_download_list_file_number()
        with allure.step("验证下载数量是否正确"):
            assert len(download_number) == len(
                check_test_data), f"下载数量错误，勾选数量：{len(download_number)}，文件数量：{len(check_test_data)}"
        with allure.step("验证下载列表下载正确"):
            result.check_download_progress(check_test_data), f"文件下载失败"
