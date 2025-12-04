import allure
import pytest

from utils.test_data_loader import load_test_data

search_check_home_page_data = load_test_data("download_large_memory_files_data.json")
copy_page_enter_folder = load_test_data("copy_page_enter_folder.json")


@pytest.mark.parametrize(
    # 声明需要传递的参数：input_name（给input_name fixture）和check_test_data（给check_test_data fixture）
    "check_test_data",
    # 参数值：按顺序对应input_name和check_test_data
    [
        (
              search_check_home_page_data[i]["search_name"],  # check_test_data的值
              copy_page_enter_folder[i]["folder_name_first"],  # 进入复制页面第一个文件夹
              copy_page_enter_folder[i]["enter_folder_second"],  # 进入复制页面第二个文件夹
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
@allure.story("复制窗口勾选文件夹")
class TestCopyPageCheckFolder:
    pass
