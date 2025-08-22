import os
import pytest
from dotenv import load_dotenv
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from utils.driver_factory import DriverFactory

# Load environment variables from .env file
load_dotenv()

@pytest.fixture(scope="function")
def driver():
    """Create WebDriver instance based on environment variables"""
    browser = os.getenv('BROWSER', 'chrome')
    headless = os.getenv('HEADLESS', 'true').lower() == 'true'
    device_name = os.getenv('DEVICE', 'desktop')  # New device parameter
    
    # Use device-specific driver creation if device is specified
    if device_name and device_name != 'custom':
        driver = DriverFactory.create_driver_for_device(
            browser=browser,
            headless=headless,
            device_name=device_name
        )
    else:
        # Fallback to custom dimensions
        screen_width = int(os.getenv('SCREEN_WIDTH', '1920'))
        screen_height = int(os.getenv('SCREEN_HEIGHT', '1080'))
        driver = DriverFactory.create_driver(
            browser=browser,
            headless=headless,
            width=screen_width,
            height=screen_height
        )
    
    # Set implicit wait from environment variable or default to 10 seconds
    implicit_wait = int(os.getenv('IMPLICIT_WAIT', '10'))
    driver.implicitly_wait(implicit_wait)
    
    yield driver
    driver.quit()

@pytest.fixture(scope="session")
def base_url():
    """Get base URL from environment"""
    return os.getenv('OLLAMA_URL', 'http://52.18.93.49:3000/')