import logging
import os

from appium.options.android import UiAutomator2Options

from base.base_page import BasePage
from utils.adb_helper import ADBHelper
from utils.config_loader import load_yaml_config

config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config/config.yaml'))
config = load_yaml_config(config_path)
logger = logging.getLogger(__name__)
options = UiAutomator2Options()


class AppSwitcher(BasePage):
    CONFIG_PATH = "data/locators/bookshelf_page.yaml"
    
    def __init__(self, driver):
        super().__init__(driver)
        # 1. 从 driver capabilities 中获取设备 ID（支持多设备）
        device_id = driver.capabilities.get("deviceName") or driver.capabilities.get("udid")
        # 2. 初始化 ADBHelper，传入设备 ID
        self.adb_helper = ADBHelper(device_id=device_id)
    
    def switch_bookshelf_app(self):
        """使用 ADBHelper 执行 adb 命令切换到书架应用"""
        logger.info("=== 开始切换到书架应用 ===")
        
        # 1. 构建 startActivity 命令（基于你提供的有效 adb 命令）
        adb_command = [
            "shell", "am", "start", "-W",
            "-a", "android.intent.action.VIEW",
            "-d", "switch://hanvon.aebr.hvLauncher?to=rack",
            "-p", "hanvon.aebr.hvLauncher"
        ]
        
        try:
            # 2. 使用 ADBHelper 执行命令
            result = self.adb_helper.execute_command(adb_command)
            logger.info(f"adb 命令执行成功，输出: {result}")
            
            # 3. 验证启动结果（可选，根据实际输出调整）
            if "Error" in result or "Failed" in result:
                logger.error(f"应用启动失败，adb 输出含错误: {result}")
                raise Exception(f"书架应用启动失败: {result}")
            
            logger.info("=== 书架应用切换成功 ===")
        except Exception as e:
            logger.error(f"切换书架应用失败: {e}")
            raise
    
    def switch_hv_drive_app(self):
        """修正版：不带设备ID，切换到汉王驾驶应用"""
        logger.info("=== 开始切换到汉王驾驶应用 ===")
        
        # 读取配置（仅包名/Activity，无设备ID）
        device_config = config['device']
        drive_package = device_config.get('appPackage')
        drive_activity = device_config.get('appActivity')
        
        # 打印配置（确认包名/Activity正确）
        logger.debug(f"执行配置 → 包名：{drive_package}，Activity：{drive_activity}")
        
        # 构建和手动命令完全一致的命令（无-s参数）
        bring_foreground_cmd = [
            "shell",
            "am",
            "start",
            "-W",  # 关键：等待应用前台唤醒完成（不重启）
            "-n",
            f"{drive_package}/{drive_activity}"
        ]
        
        try:
            # 打印最终执行的命令（验证无-s）
            full_cmd = self.adb_helper.execute_command(bring_foreground_cmd)
            logger.debug(f"调前台命令：{' '.join(full_cmd)}")
        except Exception as e:
            logger.error("=== 切换失败 ===", exc_info=True)
            raise
