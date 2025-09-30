import logging
from typing import Dict, Optional

from utils.adb_helper import ADBHelper

logger = logging.getLogger(__name__)


class DeviceInfoManager:
    """设备信息管理器"""
    
    # 硬件属性映射表（支持多种属性名）
    HARDWARE_VERSION_PROPS = [
        "ro.product.hw.version",  # 你的设备使用的属性
        "ro.hardware.version",  # 备用属性1
        "ro.hw.version",  # 备用属性2
        "ro.product.hardware",  # 备用属性3
    ]
    
    def __init__(self, device_id: Optional[str] = None):
        self.adb_helper = ADBHelper(device_id)
        self._cache = {}  # 缓存设备信息
    
    def get_hardware_version(self) -> str:
        """获取硬件版本号"""
        if 'hardware_version' in self._cache:
            return self._cache['hardware_version']
        
        for prop in self.HARDWARE_VERSION_PROPS:
            version = self.adb_helper.get_property(prop)
            if version and version != "Unknown":
                self._cache['hardware_version'] = version
                logger.info(f"从属性 {prop} 获取到硬件版本: {version}")
                return version
        
        self._cache['hardware_version'] = "Unknown"
        logger.warning("未找到硬件版本信息")
        return "Unknown"
    
    def get_comprehensive_device_info(self) -> Dict[str, str]:
        """获取完整的设备信息"""
        if 'comprehensive_info' in self._cache:
            return self._cache['comprehensive_info']
        
        device_info = {
            'hardware_version': self.get_hardware_version(),
            'model': self.adb_helper.get_property("ro.product.model"),
            'manufacturer': self.adb_helper.get_property("ro.product.manufacturer"),
            'android_version': self.adb_helper.get_property("ro.build.version.release"),
            'brand': self.adb_helper.get_property("ro.product.brand"),
            'device': self.adb_helper.get_property("ro.product.device"),
        }
        
        self._cache['comprehensive_info'] = device_info
        return device_info


# 创建全局实例（单例模式）
_device_manager: Optional[DeviceInfoManager] = None


def get_device_manager(device_id: Optional[str] = None) -> DeviceInfoManager:
    """获取设备管理器实例（单例）"""
    global _device_manager
    if _device_manager is None:
        _device_manager = DeviceInfoManager(device_id)
    return _device_manager


def get_hardware_version(device_id: Optional[str] = None) -> str:
    """快速获取硬件版本号（便捷函数）"""
    return get_device_manager(device_id).get_hardware_version()
