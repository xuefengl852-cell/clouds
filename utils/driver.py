import logging
import os

from appium import webdriver
from appium.options.android import UiAutomator2Options

from utils.config_loader import load_yaml_config

config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config/config.yaml'))
config = load_yaml_config(config_path)
logger = logging.getLogger(__name__)


def init_driver():
    # 创建选项对象
    options = UiAutomator2Options()
    # 从配置加载设备能力
    device_config = config['device']
    for key, value in device_config.items():
        options.set_capability(key, value)
    
    # 创建驱动实例
    driver = webdriver.Remote(
        command_executor=config['appium']['server_url'],
        options=options
    )
    # 验证：是否成功启动目标 App（通过 appPackage 校验当前运行的 App）
    current_app = driver.current_package
    target_app = device_config.get('appPackage')
    if current_app != target_app:
        logger.error(f"初始化失败：当前运行的 App 是 {current_app}，目标 App 是 {target_app}")
        raise Exception(f"App 上下文错误：未启动目标 App {target_app}")
    logger.info(f"初始化成功：已启动目标 App {target_app}")
    driver.implicitly_wait(10)
    return driver
