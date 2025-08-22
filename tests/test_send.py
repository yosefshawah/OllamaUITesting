import pytest
import sys
import os
import unittest
from dotenv import load_dotenv

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from pages.page_factory import PageFactory
from utils.driver_factory import DriverFactory

# Load environment variables
load_dotenv()

class TestOllamaChat(unittest.TestCase):
    
    def setUp(self):
        """Set up test - runs before each test method"""
        browser = os.getenv('BROWSER', 'chrome')
        headless = os.getenv('HEADLESS', 'false').lower() == 'true'
        device_name = os.getenv('DEVICE', 'desktop')
        
        # Use device-specific driver creation
        if device_name and device_name != 'custom':
            self.driver = DriverFactory.create_driver_for_device(
                browser=browser,
                headless=headless,
                device_name=device_name
            )
        else:
            # Fallback to custom dimensions
            screen_width = int(os.getenv('SCREEN_WIDTH', '1920'))
            screen_height = int(os.getenv('SCREEN_HEIGHT', '1080'))
            self.driver = DriverFactory.create_driver(
                browser=browser,
                headless=headless,
                width=screen_width,
                height=screen_height
            )
        
        # Set implicit wait
        implicit_wait = int(os.getenv('IMPLICIT_WAIT', '10'))
        self.driver.implicitly_wait(implicit_wait)
        
        self.base_url = os.getenv('OLLAMA_URL', 'http://localhost:3000')
        self.device = device_name
        
        print(f"Running test on {device_name} device")
    
    def tearDown(self):
        """Clean up after each test - runs after each test method"""
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()
    
    def test_select_model_and_send_prompt(self, driver=None, base_url=None):
        """Test selecting a model and sending a prompt to get a response"""
        # Use unittest driver if called directly, pytest fixtures if called by pytest
        test_driver = driver if driver else self.driver
        test_base_url = base_url if base_url else self.base_url
        
        test_message = "hello world"
        
        # Initialize device-appropriate page object and chain the entire flow
        chat_page = (PageFactory.create_chat_page(test_driver)
                    .navigate_to(test_base_url)
                    .clear_app_state()
                    .select_model()
                    .enter_prompt(test_message))
        
        # Verify the text was entered correctly
        self.assertIn(test_message, chat_page.get_prompt_value(), "Prompt text was not entered correctly")
        
        # Submit and get response using chaining
        chat_page.submit_prompt()
        response_texts = chat_page.wait_for_response()
        
        # Print the response for debugging
        print(f"Model response: {response_texts}")
        
        # Assert that we got a meaningful response (more than 1 character)
        response_text = "\n".join(response_texts)
        self.assertGreater(len(response_text), 1, "Response text should be more than 1 character")
        
        print("✅ Test completed successfully!")


if __name__ == "__main__":
    # Run when executed directly (for debugging)
    unittest.main(verbosity=2)
