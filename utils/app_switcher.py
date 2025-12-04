import logging

from appium.webdriver.webdriver import WebDriver as AppiumDriver

from base.base_page import BasePage

logger = logging.getLogger(__name__)


class AppSwitcher(BasePage):
    """APP切换工具类（直接继承BasePage，复用正确的Appium驱动）"""
    
    def __init__(self, driver: AppiumDriver, timeout=None):
        """
        构造函数：适配 BasePage 的参数要求
        :param driver: Appium 驱动实例（传递给 BasePage）
        :param timeout: 超时时间（可选，传递给 BasePage）
        """
        # 调用 BasePage 的构造函数，传递必需的 driver 参数，以及可选的 timeout
        super().__init__(driver=driver, timeout=timeout)
        
        # 验证驱动类型（确保是 Appium 驱动，有 start_activity 方法）
        if not isinstance(driver, AppiumDriver):
            raise TypeError(
                f"驱动类型错误！需要 AppiumDriver，实际传入：{type(driver)}"
            )
        logger.info(f"✅ AppSwitcher 驱动类型：{type(driver)}（AppiumDriver）")
    
    def switch_to_target_app(self, target_app_info, app_locator, condition='visible'):
        """切换到目标应用（复用 BasePage 的 driver 和 wait_for_element）"""
        try:
            # 核心：调用 Appium 驱动的 start_activity（继承自 BasePage 的 self.driver）
            self.driver.start_activity(
                app_package=target_app_info["appPackage"],
                app_activity=target_app_info["appActivity"]
            )
            
            # 验证包名切换成功
            current_package = self.driver.current_package
            assert current_package == target_app_info["appPackage"], \
                f"切换失败！当前包名：{current_package}，期望：{target_app_info['appPackage']}"
            
            # 复用 BasePage 的 wait_for_element（继承获得，无需额外传递）
            element = self.wait_for_element(locator=app_locator, condition=condition)
            assert element is not None, f"目标应用元素未找到：{app_locator}"
            
            logger.info(f"✅ 成功切换到目标应用：{target_app_info['appPackage']}")
            return True
        except Exception as e:
            logger.error(f"❌ 切换目标应用失败：{str(e)}", exc_info=True)
            raise
    #
    # def switch_back_to_origin(self, origin_app_info, drive_locator, condition='visible'):
    #     """切回原应用"""
    #     try:
    #         self.driver.start_activity(
    #             app_package=origin_app_info["appPackage"],
    #             app_activity=origin_app_info["appActivity"]
    #         )
    #         current_package = self.driver.current_package
    #         assert current_package == origin_app_info["appPackage"], \
    #             f"切回失败！当前包名：{current_package}，期望：{origin_app_info['appPackage']}"
    #         element = self.wait_for_element(locator=drive_locator, condition=condition)
    #         assert element is not None, f"原应用元素未找到：{drive_locator}"
    #         logger.info(f"✅ 成功切回原应用：{origin_app_info['appPackage']}")
    #         return True
    #     except Exception as e:
    #         logger.error(f"❌ 切回原应用失败：{str(e)}", exc_info=True)
    #         raise
