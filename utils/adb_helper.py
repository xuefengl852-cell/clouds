import logging
import subprocess
from typing import Optional, List

logger = logging.getLogger(__name__)


class ADBHelper:
    """ADB命令工具类"""
    
    def __init__(self, device_id: Optional[str] = None):
        self.device_id = device_id
    
    def _build_adb_command(self, command: List[str]) -> List[str]:
        """构建ADB命令"""
        base_cmd = ["adb"]
        if self.device_id:
            base_cmd.extend(["-s", self.device_id])
        base_cmd.extend(command)
        return base_cmd
    
    def execute_command(self, command: List[str], timeout: int = 30) -> str:
        """执行ADB命令"""
        try:
            full_cmd = self._build_adb_command(command)
            logger.debug(f"执行命令: {' '.join(full_cmd)}")
            
            result = subprocess.check_output(
                full_cmd,
                stderr=subprocess.PIPE,
                timeout=timeout
            ).decode('utf-8').strip()
            
            return result
        except subprocess.TimeoutExpired:
            logger.error(f"命令执行超时: {' '.join(command)}")
            raise
        except subprocess.CalledProcessError as e:
            logger.error(f"命令执行失败: {e.stderr.decode('utf-8') if e.stderr else str(e)}")
            raise
        except Exception as e:
            logger.error(f"执行命令时发生异常: {e}")
            raise
    
    def get_property(self, prop_name: str, default: str = "Unknown") -> str:
        """获取设备属性"""
        try:
            result = self.execute_command(["shell", "getprop", prop_name])
            return result if result else default
        except Exception:
            return default
