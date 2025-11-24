import allure
import pytest

from utils.test_data_loader import load_test_data

search_check_home_page_data = load_test_data("search_check_home_page_data.json")


@allure.story("勾选文件后进行文件全选操作")
@pytest.mark.run(order=17)
class TestSelectAll:
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
    @allure.title("全选文件")
    def test_search_select_file(self, checked_interface_with_cleanup, check_test_data):
        result = checked_interface_with_cleanup
        result.set_skip_default_cleanup()
        
        def click_cancel_but():
            result.click_cancel_but()
        
        result.register_cleanup(click_cancel_but)
        with allure.step("点击全选按钮"):
            result.click_select_all_but()
        with allure.step("验证全选当前页文件"):
            check_file_name_list = result.get_select_all_element_text()
            file_check_box_status = result.verify_locator_click_status(check_file_name_list, 'true')
            assert file_check_box_status, f"验证全部点击状态失败"
        with allure.step("验证全选按钮变为取消全选"):
            assert result.get_select_all_text() == "取消全选", f"按钮状态错误"
    
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
    @allure.title("取消全选文件")
    def test_search_cancel_select_file(self, click_select_all_but, check_test_data):
        result = click_select_all_but
        with allure.step("点击取消全选按钮"):
            result.click_select_all_but()
        with allure.step("验证取消全选当前页文件"):
            search_btn_status = result.verify_search_btn_exist()
            assert search_btn_status, f"验证全部点击状态失败"
