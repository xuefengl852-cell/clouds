import os

from appium import webdriver
from appium.options.android import UiAutomator2Options

from utils.config_loader import load_yaml_config

config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config/config.yaml'))
config = load_yaml_config(config_path)


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
    driver.implicitly_wait(10)
    return driver
