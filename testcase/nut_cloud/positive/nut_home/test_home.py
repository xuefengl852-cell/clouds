import allure
import pytest


@pytest.mark.run(order=2)
@allure.epic("坚果云网盘详情页")
@allure.feature("主页登录模块")
class TestHomeScenarios:
    
    @allure.story("用户长按网盘")
    @allure.title("长按验证是否出现详情页弹窗")
    def test_long_cloud(self, nut_cloud_login_page):
        # nut_cloud_login_page.set_skip_default_cleanup()
        with allure.step("长按网盘图标"):
            result = nut_cloud_login_page.long_nut_cloud()
            assert result.get_text_long_enter_details() == '详情', f"长按坚果云网盘断言失败"
    
    @allure.story("用户点击绑定网盘")
    @allure.title("验证是否出现绑定网盘弹窗")
    def test_bind_cloud(self, nut_cloud_login_page):
        with allure.step("点击绑定网盘按钮"):
            result = nut_cloud_login_page.click_bind_cloud()
            assert result.get_text_click_bind_cloud() == '绑定网盘', f"绑定网盘弹窗弹出失败"
    
    @allure.story("用户点击更多按钮")
    @allure.title("验证是否出现更多按钮弹窗")
    def test_click_more_button(self, nut_cloud_login_page):
        result = nut_cloud_login_page.click_more_button()
        assert result.get_text_click_more_window() == '视图模式', f"更多弹窗未弹出"
    
    @allure.story("用户点击坚果云网盘")
    @allure.title("验证进入坚果云网盘")
    def test_enter_nut_cloud_home(self, nut_cloud_login_page):
        result = nut_cloud_login_page.click_cloud()
        assert result.is_folder_with_text_present('我的坚果云'), f"进入网盘主页失败"
