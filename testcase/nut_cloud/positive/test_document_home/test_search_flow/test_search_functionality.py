import ast

import allure
import pytest

from pages.nut_cloud_page.document_home_page import DocumentHomePage
from utils.test_data_loader import load_test_data

search_mode_data = load_test_data("search_mode_data.json")


@pytest.mark.run(order=11)
@allure.story("输入-搜索功能测试")
class TestSearchFunctionality:
    @pytest.mark.parametrize(
        "input_name",
        [data["search_name"] for data in search_mode_data],
        ids=[data["test_name"] for data in search_mode_data]
    )
    @allure.title("根据不同输入点击搜索按钮")
    def test_input_name_search(self, input_search_name, input_name, request):
        raw_test_name = request.node.callspec.id
        current_test_name = ast.literal_eval(f'"{raw_test_name}"')
        result = input_search_name
        
        def delete_search_name():
            document_home_page = DocumentHomePage(result.driver)
            result.navigate_back(1)
            document_home_page.click_search_button()
        
        result.register_cleanup(delete_search_name)
        with allure.step("点击搜素按钮"):
            result.click_search_button()
        with allure.step("获取搜索页列表数据"):
            search_results = result.get_all_search_document_names()
        with allure.step("验证搜索内容是否匹配"):
            if current_test_name == "精准搜索":
                # 精准搜索：断言至少有一个结果与输入完全一致
                assert any(
                    res == input_name for res in search_results
                ), f"精准搜索失败，未找到与'{input_name}'完全匹配的结果，实际结果：{search_results}"
            
            elif current_test_name in ["中文模糊匹配", "特殊符号模糊匹配", "数字模糊匹配"]:
                # 模糊匹配：断言至少有一个结果包含输入关键词
                assert any(
                    input_name in res for res in search_results
                ), f"{current_test_name}失败，未找到包含'{input_name}'的结果，实际结果：{search_results}"
            
            else:
                # 未知场景：抛出异常提醒补充断言
                pytest.fail(f"未定义[{current_test_name}]的断言逻辑，请补充")
