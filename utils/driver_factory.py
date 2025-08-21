import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions

class DriverFactory:
    @staticmethod
    def create_driver(browser='chrome', headless=True, width=1920, height=1080):
        if browser.lower() == 'chrome':
            return DriverFactory._create_chrome_driver(headless, width, height)
        elif browser.lower() == 'firefox':
            return DriverFactory._create_firefox_driver(headless, width, height)
        else:
            raise ValueError(f"Unsupported browser: {browser}")
    
    @staticmethod
    def _create_chrome_driver(headless, width, height):
        options = ChromeOptions()
        if headless:
            options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument(f'--window-size={width},{height}')
        
        driver = webdriver.Chrome(options=options)
        driver.set_window_size(width, height)
        return driver
    
    @staticmethod
    def _create_firefox_driver(headless, width, height):
        options = FirefoxOptions()
        if headless:
            options.add_argument('--headless')
        
        driver = webdriver.Firefox(options=options)
        driver.set_window_size(width, height)
        return driver