import logging
from typing import List, Tuple, Any, Optional


class LocatorValidator:
    """定位器验证工具类"""
    
    def __init__(self, logger: Optional[logging.Logger] = None):
        self.logger = logger or logging.getLogger(__name__)
        self.missing_locators = []
        self.invalid_locators = []
    
    def validate(self, page_object: Any) -> Tuple[List[str], List[str]]:
        """
        验证页面对象中的所有定位器属性
        :param page_object: 页面对象实例
        :return: (缺失的定位器列表, 无效的定位器列表)
        """
        self.missing_locators = []
        self.invalid_locators = []
        
        # 获取所有属性
        properties = self._get_locator_properties(page_object)
        
        for prop_name in properties:
            self._validate_single_locator(page_object, prop_name)
        
        return self.missing_locators, self.invalid_locators
    
    def _get_locator_properties(self, page_object: Any) -> List[str]:
        """获取所有定义为属性的定位器"""
        return [
            attr for attr in dir(page_object)
            if not attr.startswith("__") and  # 排除特殊方法
               isinstance(getattr(type(page_object), attr, None), property)
        ]
    
    def _validate_single_locator(self, page_object: Any, prop_name: str):
        """验证单个定位器属性"""
        try:
            locator = getattr(page_object, prop_name)
            
            if locator is None:
                self.missing_locators.append(prop_name)
                self.logger.warning(f"定位器缺失: {prop_name}")
            elif not self._is_valid_locator(locator):
                self.invalid_locators.append(prop_name)
                self.logger.warning(f"无效定位器格式: {prop_name} -> {locator}")
            else:
                self.logger.debug(f"定位器验证通过: {prop_name} -> {locator}")
        except Exception as e:
            self.missing_locators.append(prop_name)
            self.logger.error(f"获取定位器失败: {prop_name} - {str(e)}")
    
    @staticmethod
    def _is_valid_locator(locator) -> bool:
        """检查是否为有效的定位器"""
        # 基本格式检查：元组且长度为2
        if not (isinstance(locator, tuple) and len(locator) == 2):
            return False
        
        # 定位策略验证
        valid_strategies = ['id', 'xpath', 'name', 'class', 'css',
                            'accessibility_id', 'android', 'ios']
        if locator[0] not in valid_strategies:
            return False
        
        # 定位值非空检查
        if not locator[1] or not isinstance(locator[1], str):
            return False
        
        return True
    
    def generate_report(self) -> str:
        """生成验证报告"""
        report = ["定位器验证报告:"]
        
        if not self.missing_locators and not self.invalid_locators:
            report.append("✅ 所有定位器验证通过")
        else:
            if self.missing_locators:
                report.append(f"❌ 缺失定位器 ({len(self.missing_locators)}):")
                report.extend([f"  - {name}" for name in self.missing_locators])
            
            if self.invalid_locators:
                report.append(f"⚠️ 无效定位器格式 ({len(self.invalid_locators)}):")
                report.extend([f"  - {name}" for name in self.invalid_locators])
        
        return "\n".join(report)
