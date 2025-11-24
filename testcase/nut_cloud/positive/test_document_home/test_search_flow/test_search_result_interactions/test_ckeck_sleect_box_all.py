import allure
import pytest

from utils.test_data_loader import load_test_data

search_select_all_file_data = load_test_data("search_select_all_file.json")


@allure.story("勾选与全选交互")
class TestCheckSelectBoxAll:
    @pytest.mark.run(order=16)
    @pytest.mark.parametrize(
        # 声明需要传递的参数：input_name（给input_name fixture）和check_test_data（给check_test_data fixture）
        "check_test_data",
        # 参数值：按顺序对应input_name和check_test_data
        [
            (
                  search_select_all_file_data[i]["search_name"]  # check_test_data的值
            )
            for i in range(len(search_select_all_file_data))
        ],
        # 用例标识（可选，增强报告可读性）
        ids=[
            f"{search_select_all_file_data[i]['test_name']}_check"
            for i in range(len(search_select_all_file_data))
        ],
        # 指定参数传递给对应的fixture
        indirect=["check_test_data"]
    )
    @allure.title("全部勾选")
    def test_select_all_check_box(self, search_check_box_file, check_test_data):
        def click_cancel_select():
            search_check_box_file.click_cancel_but()
        
        search_check_box_file.register_cleanup(click_cancel_select)
        
        with allure.step("验证搜索页当前页文件全部选择后全选按钮变为取消全选"):
            assert search_check_box_file.get_select_all_text() == "取消全选", "全选文件后当前全选状态未变为取消全选"
