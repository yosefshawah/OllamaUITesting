from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
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
        try:
            self.driver.execute_script(
                "try { localStorage.clear(); } catch (e) { console.log('localStorage not available'); }"
                "try { sessionStorage.clear(); } catch (e) { console.log('sessionStorage not available'); }"
                "try { indexedDB.databases().then(dbs => dbs.forEach(db => indexedDB.deleteDatabase(db.name))); } catch (e) { console.log('indexedDB not available'); }"
            )
        except Exception as e:
            print(f"Warning: Could not clear browser storage: {e}")
        
        self.driver.refresh()
        # Wait for page to be fully loaded
        self.wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
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
        submit_button = self.wait.until(EC.presence_of_element_located(self.SUBMIT_BUTTON))
        
        # Wait for button to be enabled
        self.wait.until(lambda d: submit_button.is_enabled())
        
        # Scroll to button and click
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", 
            submit_button
        )
        
        # Wait for button to be clickable after scrolling
        self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON)).click()
        return self
    
    def wait_for_response(self, timeout=20):
        """Wait for AI response to appear next to ollama.png and return response text"""
        # Create a longer wait for response timeout
        response_wait = WebDriverWait(self.driver, timeout)
        
        # Wait for ollama.png image to appear (indicates response started)
        ollama_img = response_wait.until(
            EC.presence_of_element_located((By.XPATH, "//img[@src='/ollama.png']"))
        )
        print("Found ollama.png image")
        
        # Find the container that has the ollama image and look for p tags nearby
        # Look for p tags that are siblings or descendants of the same container
        response_xpath = "//img[@src='/ollama.png']/ancestor::div[1]//p | //img[@src='/ollama.png']/following-sibling::*/descendant-or-self::p"
        
        # Wait for response text to stabilize (no new text being added)
        last_text = ""
        stable_count = 0
        max_attempts = 20
        
        while stable_count < 3 and max_attempts > 0:
            try:
                response_paragraphs = self.driver.find_elements(By.XPATH, response_xpath)
                current_text = "\n".join([p.text.strip() for p in response_paragraphs if p.text.strip()])
                
                if current_text and current_text == last_text:
                    stable_count += 1
                elif current_text:
                    stable_count = 0
                    last_text = current_text
                
            except Exception as e:
                print(f"Error finding response: {e}")
            
            max_attempts -= 1
            sleep(0.5)  # Short sleep to check for changes
        
        # Get final response
        try:
            response_paragraphs = self.driver.find_elements(By.XPATH, response_xpath)
            response_texts = [p.text.strip() for p in response_paragraphs if p.text.strip()]
        except Exception as e:
            print(f"Error getting final response: {e}")
            response_texts = []
        
        return response_texts
    
    def send_message_and_get_response(self, message):
        """Complete flow: enter message, submit, and get response"""
        self.enter_prompt(message)
        self.submit_prompt()
        return self.wait_for_response()
