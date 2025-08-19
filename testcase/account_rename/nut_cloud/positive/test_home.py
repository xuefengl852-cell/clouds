import allure


@allure.epic("坚果云网盘详情页")
@allure.feature("主页登录模块")
class TestHomeScenarios:
    
    @allure.story("用户长按网盘")
    @allure.title("长按验证是否出现详情页弹窗")
    def test_long_cloud(self, logged_in_home_page):
        with allure.step("长按网盘图标"):
            result = logged_in_home_page.long_nut_cloud()
            assert result.get_text_long_enter_details() == '', f"长按坚果云网盘断言失败"
    
    @allure.story("用户点击绑定网盘")
    @allure.title("验证是否出现绑定网盘弹窗")
    def test_bind_cloud(self, logged_in_home_page):
        with allure.step("点击绑定网盘按钮"):
            result = logged_in_home_page.click_bind_cloud()
            assert result.assert_bind_cloud_window(), f"绑定网盘弹窗弹出失败"
    
    @allure.story("用户点击更多按钮")
    @allure.title("验证是否出现更多按钮弹窗")
    def test_click_more_button(self, logged_in_home_page):
        result = logged_in_home_page.click_more_button()
        assert result.assert_more_window(), f"更多弹窗未弹出"
    
    @allure.story("用户点击坚果云网盘")
    @allure.title("验证进入坚果云网盘")
    def test_enter_nut_cloud_home(self, logged_in_home_page):
        result = logged_in_home_page.click_cloud()
        assert result.assert_click_enter_nut_cloud(), f"未进入坚果云网盘主界面"
