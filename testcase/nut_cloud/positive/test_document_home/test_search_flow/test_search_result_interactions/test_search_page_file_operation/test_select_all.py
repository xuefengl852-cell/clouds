import allure
import pytest

from utils.test_data_loader import load_test_data

check_data = load_test_data("search_results_check_data.json")


@allure.story("勾选文件后进行文件全选操作")
@pytest.mark.run(order=16)
class TestSelectAll:
    @pytest.mark.parametrize(
        "check_test_data",  # 参数名（对应fixture名）
        # 参数值：直接提取check_data中的search_name，避免多余的元组嵌套
        [check_data[i]["search_name"] for i in range(len(check_data))],
        # 用例标识
        ids=[f"{check_data[i]['test_name']}" for i in range(len(check_data))],
        # 仅对check_test_data启用间接传递（正确指向fixture）
        indirect=["check_test_data"]  # 推荐用列表形式，更清晰
    )
    @allure.title("全选文件")
    def test_search_select_file(self, checked_interface_with_cleanup):
        pass
