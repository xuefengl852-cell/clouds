import allure
import pytest


@pytest.mark.run(order=14)
@allure.story("搜索页面进行翻页")
class TestPaginationOperations:
    
    @allure.title("搜索页点击下一页翻页按钮")
    def test_click_next_page_but(self, enter_search_page):
        result = enter_search_page
        
        def click_pre_page_but():
            result.click_pre_page_but()
        
        result.register_cleanup(click_pre_page_but)
        
        current_page, all_pages = result.get_page_number_text()
        with allure.step("点击下一页按钮"):
            result.click_next_page_but()
        next_current_page, next_all_pages = result.get_page_number_text()
        with allure.step("验证下一页翻页成功"):
            assert current_page + 1 == next_current_page, f"点击下一页按钮失败，翻页前页码：{current_page}，翻页后页码：{next_current_page}"
    
    @allure.title("搜索页点击上一页翻页按钮")
    def test_click_next_page_but(self, click_next_page_button):
        result = click_next_page_button
        
        current_page, all_pages = result.get_page_number_text()
        with allure.step("点击上一页按钮"):
            result.click_pre_page_but()
        pre_current_page, pre_all_pages = result.get_page_number_text()
        with allure.step("验证上一页翻页成功"):
            assert current_page - 1 == pre_current_page, f"点击上一页按钮失败，翻页前页码：{current_page}，翻页后页码：{pre_current_page}"
