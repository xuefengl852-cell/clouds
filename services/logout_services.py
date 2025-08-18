import logging

from base.base_page import BasePage
from locators.login_locators import LoginLocators
from pages.nut_cloud_page.home_page import HomePage
from utils.loactor_validator import LocatorValidator

locators = LoginLocators()
locator_validator = LocatorValidator()
logger = logging.getLogger(__name__)


class LogoutServices(BasePage):
    
    def __init__(self, driver):
        super().__init__(driver)
        locator_validator.validate(self)
    
    @property
    def rename_button(self):
        return self.get_locator(locators.PAGE_SECTION, locators.BIND_CLOUD)
    
    def logout_from_anywhere(self):
        current_page = self.page_detector.detect_current_page()
        
        if current_page == 'HomePage':
            self._logout_from_home()
        else:
            self._universal_logout()
    
    def _logout_from_home(self):
        HomePage.long_press_cloud()
    
    def _universal_logout(self):
        pass
