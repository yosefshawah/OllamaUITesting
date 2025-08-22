from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from utils.device_config import DeviceConfig

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.device_config = self._detect_device_config()
    
    def _detect_device_config(self):
        """Detect current device configuration based on window size"""
        try:
            size = self.driver.get_window_size()
            width = size['width']
            breakpoint = DeviceConfig.get_breakpoint(width)
            return DeviceConfig.get_device_config(breakpoint)
        except:
            return DeviceConfig.DESKTOP
    
    def is_mobile(self):
        """Check if current device is mobile"""
        return DeviceConfig.is_mobile_device(self.device_config)
    
    def is_desktop(self):
        """Check if current device is desktop"""
        return not self.is_mobile()
    
    def get_locator(self, mobile_locator, desktop_locator):
        """Get appropriate locator based on device type"""
        return mobile_locator if self.is_mobile() else desktop_locator
    
    def is_element_present(self, locator):
        try:
            self.wait.until(EC.presence_of_element_located(locator))
            return True
        except TimeoutException:
            return False
    
    def click_element(self, locator):
        element = self.wait.until(EC.element_to_be_clickable(locator))
        element.click()
    
    def enter_text(self, locator, text):
        element = self.wait.until(EC.presence_of_element_located(locator))
        element.clear()
        element.send_keys(text)
    
    def scroll_to_element(self, locator):
        """Scroll to element - behavior may differ on mobile vs desktop"""
        element = self.wait.until(EC.presence_of_element_located(locator))
        if self.is_mobile():
            # Mobile-specific scrolling
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", element)
        else:
            # Desktop scrolling
            self.driver.execute_script("arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", element)
        return element