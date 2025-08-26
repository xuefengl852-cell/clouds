import allure


@allure.epic("更多功能点击排序")
@allure.feature("网盘排序")
class TestCloudSort:
    
    @allure.story("用户点击取消")
    @allure.title("验证回到首页")
    def test_click_cancel_button(self, cloud_sort_button):
        with allure.step("点击取消"):
            result = cloud_sort_button.click_cancel()
            assert result.verify_click_cancel_success(), f"点击取消失败"
    
    @allure.story("用户点击确定")
    @allure.title("验证回到首页")
    def test_click_sure_button(self, cloud_sort_button):
        with allure.step("点击确定"):
            result = cloud_sort_button.click_sure()
            assert result.verify_click_cancel_success(), f"点击确定失败"
    
    @allure.story("用户选择添加时间")
    @allure.title("验证排序规则无误")
    def test_click_add_time(self, cloud_sort_button):
        with allure.step("选择添加时间"):
            result = cloud_sort_button.click_add_time()
            result.get_add_time_button_clickable()
            assert result.get_add_time_button_clickable() == 'true', f"选择添加时间失败"
            result.back()
    
    @allure.story("用户选择名称")
    @allure.title("验证排序规则无误")
    def test_click_name(self, cloud_sort_button):
        with allure.step("选择名称"):
            result = cloud_sort_button.click_name()
            assert result.get_name_button_clickable() == 'true', f"选择升序失败"
            result.back()
    
    @allure.story("用户选择类型")
    @allure.title("验证排序规则无误")
    def test_click_type(self, cloud_sort_button):
        with allure.step("选择升序"):
            result = cloud_sort_button.click_asc_order()
            assert result.get_type_button_clickable() == 'true', f"选择升序失败"
            result.back()
    
    @allure.story("用户选择升序")
    @allure.title("验证排序规则无误")
    def test_click_asc(self, cloud_sort_button):
        with allure.step("选择升序"):
            result = cloud_sort_button.click_asc_order()
            assert result.get_asc_order_button_clickable() == 'true', f"选择升序失败"
            result.back()
    
    @allure.story("用户选择降序")
    @allure.title("验证排序规则无误")
    def test_click_desc(self, cloud_sort_button):
        with allure.step("选择降序"):
            result = cloud_sort_button.click_desc_order()
            assert result.get_desc_order_button_clickable() == 'true', f"选择升序失败"
            result.back()
    
    @allure.story("用户选择添加时间升序排序")
    @allure.title("验证排序规则无误")
    def test_click_add_time_asc(self, cloud_sort_button):
        with allure.step("选择添加时间"):
            result = cloud_sort_button.click_add_time()
            assert result.get_add_time_button_clickable() == 'true', f"选择添加时间失败"
        with allure.step("选择升序"):
            result.click_asc_order()
            assert result.get_asc_order_button_clickable() == 'true', f"选择升序失败"
            result.back()
    
    @allure.story("用户选择添加时间降序排序")
    @allure.title("验证排序规则无误")
    def test_click_add_time_desc(self, cloud_sort_button):
        with allure.step("选择添加时间"):
            result = cloud_sort_button.click_add_time()
            assert result.get_add_time_button_clickable() == 'true', f"选择添加时间失败"
        with allure.step("选择降序"):
            result.click_desc_order()
            assert result.get_asc_order_button_clickable() == 'true', f"选择升序失败"
            result.back()
    
    @allure.story("用户选择添加时间升序排序点击确定")
    @allure.title("验证排序规则无误")
    def test_click_add_time_asc_sure(self, cloud_sort_button):
        with allure.step("选择添加时间"):
            result = cloud_sort_button.click_add_time()
            assert result.get_add_time_button_clickable() == 'true', f"选择添加时间失败"
        with allure.step("选择升序"):
            result.click_asc_order()
            assert result.get_asc_order_button_clickable() == 'true', f"选择升序失败"
        with allure.step("点击确定"):
            result.click_sure()
            assert result.verify_click_cancel_success(), f"点击确定失败"
    
    @allure.story("用户选择添加时间降序排序")
    @allure.title("验证排序规则无误")
    def test_click_add_time_desc_sure(self, cloud_sort_button):
        with allure.step("选择添加时间"):
            result = cloud_sort_button.click_add_time()
            assert result.get_add_time_button_clickable() == 'true', f"选择添加时间失败"
        with allure.step("选择降序"):
            result.click_desc_order()
            assert result.get_asc_order_button_clickable() == 'true', f"选择升序失败"
        with allure.step("点击确定"):
            result.click_sure()
            assert result.verify_click_cancel_success(), f"点击确定失败"
    
    @allure.story("用户选择名称升序排序点击确定")
    @allure.title("验证排序规则无误")
    def test_click_name_asc_sure(self, cloud_sort_button):
        with allure.step("选择名称"):
            result = cloud_sort_button.click_name()
            assert result.get_name_button_clickable() == 'true', f"选择添加时间失败"
        with allure.step("选择升序"):
            result.click_asc_order()
            assert result.get_asc_order_button_clickable() == 'true', f"选择升序失败"
        with allure.step("点击确定"):
            result.click_sure()
            assert result.verify_click_cancel_success(), f"点击确定失败"
    
    @allure.story("用户选择名称降序排序点击确定")
    @allure.title("验证排序规则无误")
    def test_click_name_desc_sure(self, cloud_sort_button):
        with allure.step("选择名称"):
            result = cloud_sort_button.click_name()
            assert result.get_name_button_clickable() == 'true', f"选择添加时间失败"
        with allure.step("选择降序"):
            result.click_desc_order()
            assert result.get_desc_order_button_clickable() == 'true', f"选择升序失败"
        with allure.step("点击确定"):
            result.click_sure()
            assert result.verify_click_cancel_success(), f"点击确定失败"
    
    @allure.story("用户选择类型升序排序点击确定")
    @allure.title("验证排序规则无误")
    def test_click_type_asc_sure(self, cloud_sort_button):
        with allure.step("选择类型"):
            result = cloud_sort_button.click_type()
            assert result.get_type_button_clickable() == 'true', f"选择添加时间失败"
        with allure.step("选择降序"):
            result.click_asc_order()
            assert result.get_asc_order_button_clickable() == 'true', f"选择升序失败"
        with allure.step("点击确定"):
            result.click_sure()
            assert result.verify_click_cancel_success(), f"点击确定失败"
    
    @allure.story("用户选择类型降序排序点击确定")
    @allure.title("验证降序规则无误")
    def test_click_type_desc_sure(self, cloud_sort_button):
        with allure.step("选择类型"):
            result = cloud_sort_button.click_type()
            assert result.get_type_button_clickable() == 'true', f"选择添加时间失败"
        with allure.step("选择降序"):
            result.click_desc_order()
            assert result.get_desc_order_button_clickable() == 'true', f"选择升序失败"
        with allure.step("点击确定"):
            result.click_sure()
            assert result.verify_click_cancel_success(), f"点击确定失败"
