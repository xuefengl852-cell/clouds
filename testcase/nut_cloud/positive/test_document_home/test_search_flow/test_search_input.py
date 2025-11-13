import logging
import random

import allure
import pytest

from utils.test_data_loader import load_test_data

search_input_data = load_test_data("search_input_name.json")
logger = logging.getLogger(__name__)
target_test_name = "中文名称输入"
filtered_data = [item for item in search_input_data if item["test_name"] == target_test_name]


@pytest.mark.run(order=10)
@allure.story("输入框输入测试")
class TestSearchInput:
    @pytest.mark.parametrize(
        "search_name",
        [data["search_name"] for data in search_input_data],
        ids=[data["test_name"] for data in search_input_data]
    )
    @allure.title("输入关键词")
    def test_search_input(self, enter_search_page, search_name):
        def delete_search_name():
            enter_search_page.click_clear_button()
        
        enter_search_page.register_cleanup(delete_search_name)
        with allure.step(f"搜索框输入内容"):
            enter_search_page.input_search_name(search_name)
        search_text = enter_search_page.get_search_text()
        with allure.step(f"验证输入内容与搜索框内容一致"):
            assert search_text == search_name, f"输入框内容：{search_text}与输入内容：{search_input_data}不一致"
    
    @allure.title("输入内容后点击回退按钮")
    @pytest.mark.parametrize("input_name", [random.choice(search_input_data)["search_name"]])
    def test_click_clear_button(self, input_search_name, input_name):
        with allure.step("点击回退"):
            input_search_name.click_clear_button()
        search_text = input_search_name.get_search_text()
        with allure.step("验证输入框内容为默认"):
            assert search_text == '请输入搜索文件名', f"点击回退按钮失败，输入框内容为：{search_text}"
