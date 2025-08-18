import logging
import os

import yaml

logger = logging.getLogger(__name__)


def load_yaml_config(file_path: str) -> dict:
    """
    加载YAML配置文件并返回字典
    :param file_path: 配置文件绝对路径
    :return: 配置字典
    """
    try:
        # 确保文件存在
        if not os.path.exists(file_path):
            logger.error(f"文件路径不存在: {file_path}")
            return {}
        
        with open(file_path, 'r', encoding='utf-8') as file:
            config = yaml.safe_load(file)
            # 验证配置类型
            if not isinstance(config, dict):
                logger.error(f"配置文件内容不是字典:  {file_path}")
                return {}
            
            return config
    except yaml.YAMLError as e:
        logger.error(f"YAML解析错误: {file_path} - {e}")
        return {}
    except Exception as e:
        logger.error(f"加载配置文件失败: {file_path} - {e}")
        return {}
