import json
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def load_test_data(filename: str) -> list:
    """加载测试数据文件（带详细错误处理）"""
    try:
        # 获取项目根目录
        project_root = Path(__file__).resolve().parent.parent
        logger.info(f"项目根目录: {project_root}")
        
        # 构建完整文件路径
        test_data_dir = project_root / "data" / "test_data"
        file_path = test_data_dir / filename
        
        logger.info(f"完整文件路径: {file_path}")
        logger.info(f"文件存在: {file_path.exists()}")
        
        # 检查文件是否存在
        if not file_path.exists():
            logger.error(f"❌ 测试数据文件不存在: {file_path}")
            return []
        
        # 加载并返回数据
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            return data
    
    except json.JSONDecodeError as e:
        logger.error(f"❌ JSON 解析错误: {e}")
        return []
    except Exception as e:
        logger.exception(f"❌ 加载测试数据时发生未知错误: {e}")
        return []
