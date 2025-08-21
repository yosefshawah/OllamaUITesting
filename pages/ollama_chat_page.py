from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from time import sleep
from .base_page import BasePage

class OllamaChatPage(BasePage):
    # Locators
    SELECT_MODEL_BUTTON = (By.XPATH, "//button[normalize-space(text())='Select model']")
    MODEL_DIALOG = (By.XPATH, '//div[@role="dialog"]')
    FIRST_MODEL_BUTTON = (By.XPATH, '//div[@role="dialog"]//button')
    PROMPT_INPUT = (By.CSS_SELECTOR, '[placeholder="Enter your prompt here"]')
    SUBMIT_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"]')
    AVATAR_IMG = (By.CSS_SELECTOR, 'img[alt="Avatar"]')
    
    def __init__(self, driver):
        super().__init__(driver)
    
    def navigate_to(self, url):
        """Navigate to the Ollama chat page"""
        self.driver.get(url)
        return self
    
    def clear_app_state(self):
        """Clear browser storage and refresh page"""
        self.driver.execute_script(
            "localStorage.clear(); sessionStorage.clear(); "
            "indexedDB.databases().then(dbs => dbs.forEach(db => indexedDB.deleteDatabase(db.name)));"
        )
        self.driver.refresh()
        sleep(2)
        return self
    
    def select_model(self):
        """Click select model button and choose the first available model"""
        # Click the "Select model" button
        self.click_element(self.SELECT_MODEL_BUTTON)
        
        # Wait for dialog to appear and click first model
        self.click_element(self.FIRST_MODEL_BUTTON)
        return self
    
    def enter_prompt(self, text):
        """Enter text in the prompt input field"""
        self.enter_text(self.PROMPT_INPUT, text)
        return self
    
    def get_prompt_value(self):
        """Get the current value of the prompt input"""
        element = self.wait.until(EC.presence_of_element_located(self.PROMPT_INPUT))
        return element.get_attribute("value")
    
    def submit_prompt(self):
        """Click the submit button to send the prompt"""
        submit_button = self.driver.find_element(*self.SUBMIT_BUTTON)
        
        # Wait for button to be enabled
        self.wait.until(lambda d: submit_button.is_enabled())
        
        # Scroll to button and click
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", 
            submit_button
        )
        sleep(2)
        submit_button.click()
        return self
    
    def wait_for_response(self, timeout=20):
        """Wait for AI response to appear and return response text"""
        # Wait for avatar to appear (indicates response started)
        avatar_img = self.wait.until(
            EC.presence_of_element_located(self.AVATAR_IMG)
        )
        
        # Traverse to get the response container
        avatar_container = avatar_img.find_element(By.XPATH, './ancestor::div[1]')
        response_div = avatar_container.find_element(By.XPATH, 'following-sibling::div[1]')
        
        # Wait a bit for response to complete
        sleep(3)
        
        # Collect all paragraphs in the response
        response_paragraphs = response_div.find_elements(By.TAG_NAME, 'p')
        response_texts = [p.text.strip() for p in response_paragraphs if p.text.strip()]
        
        return response_texts
    
    def send_message_and_get_response(self, message):
        """Complete flow: enter message, submit, and get response"""
        self.enter_prompt(message)
        self.submit_prompt()
        return self.wait_for_response()
