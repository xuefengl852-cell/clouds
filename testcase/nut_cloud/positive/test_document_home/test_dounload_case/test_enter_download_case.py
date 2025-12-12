import allure
import pytest


@pytest.mark.run(order=28)
@allure.story("传输按钮交互")
class TestEnterDownloadCase:
    
    @allure.title("进入传输列表")
    def test_enter_download_page(self, enter_folder_page):
        pass
