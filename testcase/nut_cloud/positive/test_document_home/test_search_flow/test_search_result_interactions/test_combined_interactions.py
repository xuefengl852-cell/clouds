import allure
import pytest

from utils.test_data_loader import load_test_data

search_check_home_page_data = load_test_data("search_check_home_page_data.json")


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
@pytest.mark.run(order=15)
@allure.story("勾选文件与翻页交互")
class TestCombinedInteractions:
    
    @allure.title("勾选后向后翻页")
    def test_check_file_next(self, search_check_box_file, check_test_data):
        result = search_check_box_file
        
        def click_pre_page_but():
            result.click_pre_page_but()
        
        result.register_cleanup(click_pre_page_but)
        current_page, all_pages = result.get_page_number_text()
        with allure.step("点击下一页按钮"):
            result.click_next_page_but()
        next_current_page, next_all_pages = result.get_page_number_text()
        with allure.step("验证下一页翻页成功"):
            assert current_page + 1 == next_current_page, f"点击下一页按钮失败，翻页前页码：{current_page}，翻页后页码：{next_current_page}"
        with allure.step("验证翻页后退出操作栏"):
            assert result.verify_search_btn_exist(), f"验证翻页后操作栏不存在失败"
