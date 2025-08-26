"""Page Factory to create appropriate page objects based on device type"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.device_config import DeviceConfig
from .ollama_chat_mobile import OllamaChatMobilePage
from .ollama_chat_desktop import OllamaChatDesktopPage
from .sidebar_page import SidebarPage

class PageFactory:
    """Factory class to create device-appropriate page objects"""
    
    @staticmethod
    def create_chat_page(driver):
        """Create appropriate chat page based on driver's device type"""
        # Detect device type from window size
        try:
            size = driver.get_window_size()
            width = size['width']
            breakpoint = DeviceConfig.get_breakpoint(width)
            device_config = DeviceConfig.get_device_config(breakpoint)
            
            print(f"Creating chat page for {device_config['name']} device (width: {width}px)")
            
            if DeviceConfig.is_mobile_device(device_config):
                return OllamaChatMobilePage(driver)
            else:
                return OllamaChatDesktopPage(driver)
                
        except Exception as e:
            print(f"Error detecting device type: {e}, defaulting to desktop")
            return OllamaChatDesktopPage(driver)

    @staticmethod
    def create_sidebar_page(driver):
        """Create SidebarPage (single implementation handles mobile differences)."""
        return SidebarPage(driver)
    
    @staticmethod
    def create_chat_page_for_device(driver, device_name):
        """Create chat page for specific device type"""
        device_config = DeviceConfig.get_device_config(device_name)
        
        print(f"Creating chat page for {device_config['name']} device")
        
        if DeviceConfig.is_mobile_device(device_config):
            return OllamaChatMobilePage(driver)
        else:
            return OllamaChatDesktopPage(driver)

    @staticmethod
    def create_sidebar_page_for_device(driver, device_name):
        """Create SidebarPage for specific device type (API parity)."""
        return SidebarPage(driver)
    
    @staticmethod
    def get_supported_devices():
        """Get list of supported device types"""
        return ['mobile', 'tablet', 'desktop', 'desktop_small']
