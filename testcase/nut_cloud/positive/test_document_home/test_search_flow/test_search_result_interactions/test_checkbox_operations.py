import logging

import allure
import pytest

from utils.test_data_loader import load_test_data

logger = logging.getLogger(__name__)
check_data = load_test_data("search_results_check_data.json")
search_mode_data = load_test_data("search_mode_data.json")


@allure.story("搜索结果勾选")
@pytest.mark.parametrize(
    # 声明需要传递的参数：input_name（给input_name fixture）和check_test_data（给check_test_data fixture）
    "input_name, check_test_data",
    # 参数值：按顺序对应input_name和check_test_data
    [
        (
              search_mode_data[i]["search_name"],  # input_name的值
              check_data[i]["search_name"]  # check_test_data的值
        )
        for i in range(min(len(search_mode_data), len(check_data)))
    ],
    # 用例标识（可选，增强报告可读性）
    ids=[
        f"{search_mode_data[i]['test_name']}_check"
        for i in range(min(len(search_mode_data), len(check_data)))
    ],
    # 指定参数传递给对应的fixture
    indirect=["input_name", "check_test_data"]
)
@pytest.mark.run(order=12)
@allure.story("搜索结果交互")
class TestCheckboxOperations:
    
    def test_search_results_check_box(self, click_search_but, check_test_data, input_name):
        result = click_search_but
        
        def cancel_click():
            result.click_cancel_but()
        
        result.register_cleanup(cancel_click)
        with allure.step("根据文件夹名称进行勾选文件"):
            result.click_search_file_name(check_test_data)
        
        with allure.step("验证文件是否已被勾选"):
            assert result.verify_locator_click_status(check_test_data, 'true'), f"文件:{check_test_data}勾选失败"
        with allure.step("验证文件选择个数"):
            select_number = result.get_locator_select_number()
            assert len(
                check_test_data) == select_number, f"文件点击选择个数失败。获取数量：{select_number},实际数量：{len(check_test_data)}"
    
    def test_cancel_checkbox(self, click_file_checkbox, check_test_data, input_name):
        def click_delete_bun():
            click_file_checkbox.click_clear_button()
        
        click_file_checkbox.register_cleanup(click_delete_bun)
        
        with allure.step(f"点击取消按钮"):
            click_file_checkbox.click_cancel_but()
        with allure.step(f"验证去点击取消成功"):
            assert click_file_checkbox.verify_cancel_but_not_success, f"取消按钮点击失败"
