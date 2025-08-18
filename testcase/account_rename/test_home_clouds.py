import allure
import pytest

from utils.test_data_loader import load_test_data

cloud_index_data = load_test_data("home_clouds.json")


@allure.epic("坚果云网盘首页点击网盘测试")
@allure.feature("绑定网盘")
class TestHomeClouds:
    @pytest.mark.parametrize(
        "cloud_index",
        cloud_index_data,  # 直接从JSON加载的数据
        ids=lambda case: case["test_name"]  # 使用test_name作为测试ID
    )
    @allure.story("用户可根据索引进行点击对应网盘")
    @allure.title("验证首页网盘全部可以点击")
    def test_click_nut_cloud(self, setup, cloud_index):
        with allure.step("网盘点击"):
            allure.dynamic.title(cloud_index['test_name'])
            result = setup.click_nut_cloud(cloud_index['index'])
            assert result.is_cloud_home_resource_id_visible(cloud_index['cloud_type']) == cloud_index['text'], \
                f"点击{cloud_index['cloud_type']} 网盘失败"
            result.back()
