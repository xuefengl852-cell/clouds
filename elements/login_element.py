import logging

from utils.loactor_validator import LocatorValidator

logger = logging.getLogger(__name__)


class LoginElements:
    
    def _validate_locators(self):
        """验证所有定位器属性"""
        validator = LocatorValidator(logger)
        missing, invalid = validator.validate(self)
        if missing or invalid:
            logger.error(validator.generate_report())
            raise
        else:
            logger.info("✅ 所有页面定位器验证通过")
    
    def validate_locators(self):
        """公共方法：验证所有定位器属性"""
        self._validate_locators()
