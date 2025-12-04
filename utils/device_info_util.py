# utils/app_config.py
import os

from utils.config_loader import load_yaml_config

# 读取主配置文件（和 init_driver 保持一致的路径）
config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../config/config.yaml'))
CONFIG = load_yaml_config(config_path)

# 应用配置（对应原来的 app_info 夹具内容）
APP_INFO_CONFIG = {
    # 原应用（从 config['device'] 读取）
    "origin": {
        "appPackage": CONFIG["device"]["appPackage"],
        "appActivity": CONFIG["device"]["appActivity"],
    },
    # 书架应用（从 config['target_app'] 读取）
    "bookshelf_app": {
        "appPackage": CONFIG["bookshelf_app"]["appPackage"],
        "appActivity": CONFIG["bookshelf_app"]["appActivity"],
    }
}
