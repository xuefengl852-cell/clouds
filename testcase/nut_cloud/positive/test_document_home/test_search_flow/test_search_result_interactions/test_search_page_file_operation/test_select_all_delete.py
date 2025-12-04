import allure
import pytest

from utils.test_data_loader import load_test_data

search_check_home_page_data = load_test_data("search_check_home_page_data.json")


@pytest.mark.run(order=26)
@allure.story("全选-删除组合交互")
class TestSelectAllCopy:
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
    @allure.title("全选删除")
    def test_select_all_copy(self, click_select_all_but, check_test_data):
        result = click_select_all_but
        
        def enter_search_page():
            result.click_cancel_delete_btn()
            result.navigate_back(1)
            result.click_search_document_but()
        
        result.register_cleanup(enter_search_page)
        with allure.step("点击删除按钮"):
            result.click_search_delete_btn()
        
        with allure.step("验证删除提示框是否正确"):
            assert result.verify_delete_prompt_box_success(), f"删除提示框未正确弹出"
