import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from .device_config import DeviceConfig

class DriverFactory:
    @staticmethod
    def create_driver(browser='chrome', headless=True, width=1920, height=1080, device_config=None):
        """Create driver with optional device configuration"""
        if device_config:
            width = device_config['width']
            height = device_config['height']
            user_agent = device_config.get('user_agent')
        else:
            user_agent = None
            
        if browser.lower() == 'chrome':
            return DriverFactory._create_chrome_driver(headless, width, height, user_agent)
        elif browser.lower() == 'firefox':
            return DriverFactory._create_firefox_driver(headless, width, height, user_agent)
        else:
            raise ValueError(f"Unsupported browser: {browser}")
    
    @staticmethod
    def create_driver_for_device(browser='chrome', headless=True, device_name='desktop'):
        """Create driver for specific device type"""
        device_config = DeviceConfig.get_device_config(device_name)
        return DriverFactory.create_driver(browser, headless, device_config=device_config)
    
    @staticmethod
    def _create_chrome_driver(headless, width, height, user_agent=None):
        options = ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument(f'--window-size={width},{height}')
        
        if user_agent:
            options.add_argument(f'--user-agent={user_agent}')
        
        # Mobile-specific options
        if width < 768:  # Mobile breakpoint
            options.add_argument('--disable-web-security')
            options.add_argument('--disable-features=VizDisplayCompositor')
        
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(width, height)
        return driver
    
    @staticmethod
    def _create_firefox_driver(headless, width, height, user_agent=None):
        options = FirefoxOptions()
        if headless:
            options.add_argument('--headless')
        
        if user_agent:
            options.set_preference("general.useragent.override", user_agent)
        
        driver = webdriver.Firefox(options=options)
        driver.set_window_size(width, height)
        return driver