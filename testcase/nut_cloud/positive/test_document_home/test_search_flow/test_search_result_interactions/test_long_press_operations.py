import logging

import allure
import pytest

from utils.test_data_loader import load_test_data

check_data = load_test_data("search_results_check_data.json")
search_mode_data = load_test_data("search_mode_data.json")
long_file_test_data = load_test_data("long_file_data.json")
logger = logging.getLogger(__name__)


@allure.story("搜索页文件长按")
@pytest.mark.run(order=13)
class TestLongPressOperations:
    @allure.title("根据搜索结果长按文件")
    @pytest.mark.parametrize(
        # 声明需要传递的参数：input_name（给input_name fixture）和check_test_data（给check_test_data fixture）
        "input_name,check_test_data,long_file_data",
        # 参数值：按顺序对应input_name和check_test_data
        [
            (
                  search_mode_data[i]["search_name"],  # input_name的值
                  check_data[i]["search_name"],  # check_test_data的值
                  long_file_test_data[i]["search_name"]
            )
            for i in range(min(len(search_mode_data), len(check_data), len(long_file_test_data)))
        ],
        # 用例标识（可选，增强报告可读性）
        ids=[
            f"{search_mode_data[i]['test_name']}_check"
            for i in range(min(len(search_mode_data), len(check_data), len(long_file_test_data)))
        ],
        # 指定参数传递给对应的fixture
        indirect=["input_name", "check_test_data"]
    )
    def test_long_file_name(self, click_search_but, check_test_data, input_name, long_file_data):
        result = click_search_but
        
        def click_close_but():
            result.click_dialog_close()
        
        result.register_cleanup(click_close_but)
        
        current_page, all_pages = result.get_page_number_text()
        search_file_name = result.get_search_page_name_split(long_file_data[0])
        file_time, file_type, file_size = result.get_long_file_name(long_file_data[0], current_page, all_pages)
        with allure.step("搜索页长按文件"):
            result.long_press_file_name(long_file_data)
        file_main_name = result.get_file_main_name()
        file_title = result.get_file_title()
        search_page_type = result.get_file_information().lower()
        search_page_size = result.get_file_size()
        search_page_time = result.get_file_time()
        with allure.step("验证长按文件与首页名称一致"):
            assert search_file_name == file_main_name == file_title, \
                f"主页文件名称：{file_main_name}与长按后标题：{file_title}与长按文件名称：{search_file_name}不一致"
        with allure.step("验证文件类型是否相同"):
            assert file_type == search_page_type, \
                f"主页文件类型：{file_type}与长按文件类型：{search_page_type.lower()}不一致"
        with allure.step("验证文件大小是否一致"):
            assert file_size == search_page_size, \
                f"主页文件大小：{file_size}与长按文件大小：{search_page_size}不一致"
        with allure.step(f"验证文件时间是否一致"):
            assert file_time == search_page_time, \
                f"主页文件时间：{file_time}与长按文件时间：{search_page_time}不一致"
    
    @pytest.mark.parametrize(
        # 声明需要传递的参数：input_name（给input_name fixture）和check_test_data（给check_test_data fixture）
        "input_name,check_test_data,long_file_data",
        # 参数值：按顺序对应input_name和check_test_data
        [
            (
                  search_mode_data[i]["search_name"],  # input_name的值
                  check_data[i]["search_name"],  # check_test_data的值
                  long_file_test_data[i]["search_name"]
            )
            for i in range(min(len(search_mode_data), len(check_data), len(long_file_test_data)))
        ],
        # 用例标识（可选，增强报告可读性）
        ids=[
            f"{search_mode_data[i]['test_name']}_check"
            for i in range(min(len(search_mode_data), len(check_data), len(long_file_test_data)))
        ],
        # 指定参数传递给对应的fixture
        indirect=["input_name", "check_test_data", "long_file_data"]
    )
    @allure.title("关闭长按弹出窗口")
    def test_click_close_but(self, long_file_name, long_file_data, check_test_data, input_name):
        result = long_file_name
        with allure.step("点击关闭按钮"):
            result.click_dialog_close()
        with allure.step("验证关闭弹窗成功"):
            assert result.verify_file_name_None, f"关闭弹窗失败"
