import logging

import allure
import pytest

logger = logging.getLogger(__name__)


@pytest.mark.run(order=7)
@allure.epic("网盘首页点击更多按钮出现弹窗")
@allure.feature("更多模块")
class TestCloudsMore:
    @allure.story("用户切换列表模式")
    @allure.title("验证是否网盘显示模式变为列表模式")
    def test_switch_list(self, cloud_more_window, logged_in_home_page):
        with allure.step("切换列表"):
            result = cloud_more_window.click_view_button()
            logged_in_home_page.click_more_button_workflow()
            logger.info(f"起始模式为：{result.get_display_text_value('text')}")
            assert result.get_display_text_value("text") == '列表模式', f"断言失败，视图模式文本未变为列表模式"
    
    @allure.story("用户切换视图模式")
    @allure.title("验证是否网盘显示模式变为视图模式")
    def test_switch_view(self, cloud_more_window, logged_in_home_page):
        with allure.step("切换视图"):
            result = cloud_more_window.click_view_button()
            logged_in_home_page.click_more_button_workflow()
            logger.info(f"起始模式为：{result.get_display_text_value('text')}")
            assert result.get_display_text_value("text") == '视图模式', f"断言失败，视图模式文本未变为列表模式"
    
    @allure.story("用户点击排序")
    @allure.title("验证点击排序后是否弹出排序窗口")
    def test_click_sort_button(self, cloud_more_window):
        with allure.step("点击排序"):
            result = cloud_more_window.click_sort_button()
            assert result.get_sort_window_text() == '排序', f"排序弹窗未正确弹出"
