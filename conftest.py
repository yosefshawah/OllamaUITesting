import pytest
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from utils.driver_factory import DriverFactory

@pytest.fixture(scope="function")
def driver():
    """Create WebDriver instance based on environment variables"""
    browser = os.getenv('BROWSER', 'chrome')
    headless = os.getenv('HEADLESS', 'true').lower() == 'true'
    screen_width = int(os.getenv('SCREEN_WIDTH', '1920'))
    screen_height = int(os.getenv('SCREEN_HEIGHT', '1080'))
    
    driver = DriverFactory.create_driver(
        browser=browser,
        headless=headless,
        width=screen_width,
        height=screen_height
    )
    
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def base_url():
    """Get base URL from environment"""
    return os.getenv('OLLAMA_URL', 'http://52.18.93.49:3000/')