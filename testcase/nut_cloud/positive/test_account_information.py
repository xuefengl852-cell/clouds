import logging

import allure

logger = logging.getLogger(__name__)


@allure.epic("长按坚果云网盘点击账户信息")
@allure.feature("账户信息模块")
class TestAccountInformationScenarios:
    
    @allure.story("用户点击账户信息按钮")
    @allure.title("验证是否进入账户信息界面")
    def test_click_return_button(self, logged_in_account_information_page):
        with allure.step("点击返回按钮"):
            result = logged_in_account_information_page.click_return_button()
            assert result.get_bind_cloud_text() == '绑定网盘', f"点击返回按钮返回网盘主页失败"
    
    @allure.story("用户点击名称编辑按钮")
    @allure.title("验证是否进入编辑按钮界面")
    def test_click_edit_button(self, logged_in_account_information_page):
        with allure.step("点击编辑"):
            try:
                result = logged_in_account_information_page.click_edit_button()
                assert result.get_account_rename_text() == '重命名', f"点击编辑按钮失败"
            finally:
                result._safe_navigate_back(3)
    
    @allure.story("用户点击解绑按钮")
    @allure.title("验证是否出现解绑提示窗口")
    def test_click_unbind_button(self, logged_in_account_information_page):
        with allure.step("点击解绑"):
            try:
                result = logged_in_account_information_page.click_unbind_button()
                assert result.get_unbind_window_text() == '是否解绑？', f"点击解绑按钮失败"
            finally:
                result._safe_navigate_back(2)
    
    @allure.story("用户点击解绑按钮后点击取消")
    @allure.title("验证是否返回到账户信息页")
    def test_click_unbind_cancel_button(self, logged_in_account_information_page):
        try:
            with allure.step("点击解绑"):
                result = logged_in_account_information_page.click_unbind_button()
                assert result.get_unbind_window_text() == '是否解绑？', f"点击解绑按钮失败"
            with allure.step("点击取消"):
                result.click_unbind_cancel_button()
                assert result.verify_return_account(), f"点击取消按钮失败"
        finally:
            result._safe_navigate_back(1)
    
    @allure.story("用户点击解绑按钮后点击确定")
    @allure.title("验证是否返回到坚果云绑定页面")
    def test_click_unbind_sure_button(self, logged_in_account_information_page):
        with allure.step("点击解绑"):
            result = logged_in_account_information_page.click_unbind_button()
            assert result.get_unbind_window_text() == '是否解绑？', f"点击解绑按钮失败"
        with allure.step("点击确定"):
            result.click_unbind_sure_button()
            assert result.verify_unbind_success(), f"点击取消按钮失败"
