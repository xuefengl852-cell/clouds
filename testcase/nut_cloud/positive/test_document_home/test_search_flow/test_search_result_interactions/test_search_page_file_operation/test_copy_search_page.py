import allure
import pytest

from utils.test_data_loader import load_test_data

search_check_home_page_data = load_test_data("search_check_home_page_data.json")


@pytest.mark.run(order=18)
@allure.story("搜索页复制")
class TestCopySearchPage:
    
    @allure.story("搜索结果勾选")
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
    @allure.title("多个复制")
    def test_single_replication(self, search_check_box_file, check_test_data):
        result = search_check_box_file
        
        def click_cancel_copy():
            result.click_dialog_cancel_btn()
            result.click_cancel_but()
        
        result.register_cleanup(click_cancel_copy)
        with allure.step("点击复制按钮"):
            result.click_copy_btn()
        with allure.step("验证出现复制弹窗"):
            assert result.get_dialog_title_text() == "复制至", f"复制弹窗未正确显示"
