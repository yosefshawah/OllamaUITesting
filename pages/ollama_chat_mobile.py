"""Mobile-specific implementation of Ollama Chat Page"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from time import sleep
from .base_page import BasePage

class OllamaChatMobilePage(BasePage):
    """Mobile-specific chat page with mobile UI patterns"""
    
    # Mobile-specific locators
    MENU_BUTTON = (By.CSS_SELECTOR, '[aria-label="Menu"], .hamburger, .mobile-menu-btn')
    SELECT_MODEL_BUTTON = (By.XPATH, "//button[contains(text(), 'Select model')] | //button[contains(@class, 'model-select')]")
    MODEL_DIALOG = (By.XPATH, '//div[@role="dialog"] | //div[contains(@class, "modal")] | //div[contains(@class, "sheet")]')
    FIRST_MODEL_BUTTON = (By.XPATH, '//div[@role="dialog"]//button | //div[contains(@class, "modal")]//button | //div[contains(@class, "sheet")]//button')
    PROMPT_INPUT = (By.CSS_SELECTOR, '[placeholder="Enter your prompt here"], textarea, input[type="text"], .message-input')
    SUBMIT_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"], .send-button, [aria-label*="send"], [aria-label*="Send"]')
    OLLAMA_IMG = (By.XPATH, "//img[@src='/ollama.png']")
    
    # Mobile-specific UI elements
    CHAT_CONTAINER = (By.CSS_SELECTOR, '.chat-container, .messages, .conversation')
    MOBILE_HEADER = (By.CSS_SELECTOR, '.mobile-header, .chat-header')
    
    def __init__(self, driver):
        super().__init__(driver)
        print("Initialized Mobile Chat Page")
    
    def navigate_to(self, url):
        """Navigate to the Ollama chat page"""
        print(f"📱 MOBILE: Navigating to {url}")
        self.driver.get(url)
        
        # Wait for mobile-specific elements to load
        self.wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
        
        # Assert page loaded successfully
        current_url = self.driver.current_url
        assert url in current_url, f"Failed to navigate to {url}. Current URL: {current_url}"
        print(f"✅ MOBILE: Successfully navigated to {current_url}")
        
        # Assert basic page structure exists
        page_title = self.driver.title
        assert page_title, "Page title is empty - page may not have loaded properly"
        print(f"✅ MOBILE: Page loaded with title: '{page_title}'")
        
        return self
    
    def clear_app_state(self):
        """Clear browser storage and refresh page"""
        print("📱 MOBILE: Clearing application state")
        
        try:
            self.driver.execute_script(
                "try { localStorage.clear(); } catch (e) { console.log('localStorage not available'); }"
                "try { sessionStorage.clear(); } catch (e) { console.log('sessionStorage not available'); }"
                "try { indexedDB.databases().then(dbs => dbs.forEach(db => indexedDB.deleteDatabase(db.name))); } catch (e) { console.log('indexedDB not available'); }"
            )
            print("✅ MOBILE: Browser storage cleared successfully")
        except Exception as e:
            print(f"⚠️ MOBILE: Warning - Could not clear browser storage: {e}")
        
        print("📱 MOBILE: Refreshing page")
        self.driver.refresh()
        
        # Wait for page to be fully loaded
        self.wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
        
        # Assert page refreshed properly
        current_url = self.driver.current_url
        assert current_url, "Current URL is empty after refresh"
        print(f"✅ MOBILE: Page refreshed successfully - URL: {current_url}")
        
        return self
    
    def open_model_selection(self):
        """Open model selection - might require opening menu first on mobile"""
        try:
            # Try to find and click menu button first (mobile pattern)
            if self.is_element_present(self.MENU_BUTTON):
                self.click_element(self.MENU_BUTTON)
                sleep(0.5)  # Brief wait for menu animation
        except:
            pass  # Menu might not be present
        
        # Now click the select model button
        self.click_element(self.SELECT_MODEL_BUTTON)
        return self
    
    def select_model(self):
        """Mobile-specific model selection flow"""
        print("📱 MOBILE: Starting model selection")
        
        # Assert select model button exists
        assert self.is_element_present(self.SELECT_MODEL_BUTTON), "Select model button not found on mobile"
        print("✅ MOBILE: Select model button found")
        
        self.open_model_selection()
        
        # Assert dialog/sheet appeared
        assert self.is_element_present(self.MODEL_DIALOG), "Model selection dialog/sheet not found on mobile"
        print("✅ MOBILE: Model selection dialog opened")
        
        # Assert first model button exists
        assert self.is_element_present(self.FIRST_MODEL_BUTTON), "First model button not found in mobile dialog"
        print("✅ MOBILE: First model button found")
        
        # Wait for dialog/sheet to appear and click first model
        self.click_element(self.FIRST_MODEL_BUTTON)
        print("✅ MOBILE: Model selected successfully")
        
        return self
    
    def enter_prompt(self, text):
        """Enter text in the mobile prompt input"""
        print(f"📱 MOBILE: Entering prompt text: '{text}'")
        
        # Assert prompt input exists
        assert self.is_element_present(self.PROMPT_INPUT), "Prompt input field not found on mobile"
        print("✅ MOBILE: Prompt input field found")
        
        # Mobile inputs might need different handling
        prompt_element = self.wait.until(EC.presence_of_element_located(self.PROMPT_INPUT))
        
        # Focus the input (important on mobile)
        prompt_element.click()
        prompt_element.clear()
        prompt_element.send_keys(text)
        
        # Assert text was entered correctly
        entered_text = prompt_element.get_attribute("value") or prompt_element.text
        assert text in entered_text, f"Text not entered correctly. Expected: '{text}', Found: '{entered_text}'"
        print(f"✅ MOBILE: Text entered successfully: '{entered_text}'")
        
        return self
    
    def get_prompt_value(self):
        """Get the current value of the prompt input"""
        element = self.wait.until(EC.presence_of_element_located(self.PROMPT_INPUT))
        return element.get_attribute("value") or element.text
    
    def submit_prompt(self):
        """Submit prompt with mobile-optimized interaction"""
        print("📱 MOBILE: Submitting prompt")
        
        # Assert submit button exists
        assert self.is_element_present(self.SUBMIT_BUTTON), "Submit button not found on mobile"
        print("✅ MOBILE: Submit button found")
        
        submit_button = self.wait.until(EC.presence_of_element_located(self.SUBMIT_BUTTON))
        
        # Scroll to submit button (mobile needs this)
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'smooth', block: 'center'});", 
            submit_button
        )
        print("✅ MOBILE: Scrolled to submit button")
        
        # Wait for button to be enabled and clickable
        self.wait.until(lambda d: submit_button.is_enabled())
        assert submit_button.is_enabled(), "Submit button is not enabled on mobile"
        print("✅ MOBILE: Submit button is enabled")
        
        self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON)).click()
        print("✅ MOBILE: Prompt submitted successfully")
        
        return self
    
    def wait_for_response(self, timeout=20):
        """Wait for AI response on mobile"""
        print("📱 MOBILE: Waiting for AI response")
        response_wait = WebDriverWait(self.driver, timeout)
        
        # Wait for ollama.png image to appear
        try:
            ollama_img = response_wait.until(
                EC.presence_of_element_located(self.OLLAMA_IMG)
            )
            print("✅ MOBILE: Found ollama.png image - response started")
        except Exception as e:
            assert False, f"Ollama response image not found on mobile within {timeout}s: {e}"
        
        # Mobile-specific response detection
        response_xpath = "//img[@src='/ollama.png']/ancestor::div[1]//p | //img[@src='/ollama.png']/following-sibling::*/descendant-or-self::p"
        
        # Wait for response text to stabilize
        print("📱 MOBILE: Waiting for response text to stabilize")
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
                print(f"⚠️ MOBILE: Error finding response: {e}")
            
            max_attempts -= 1
            sleep(0.5)
        
        # Get final response
        try:
            response_paragraphs = self.driver.find_elements(By.XPATH, response_xpath)
            response_texts = [p.text.strip() for p in response_paragraphs if p.text.strip()]
            
            # Assert we got a response
            assert len(response_texts) > 0, "No response text found on mobile"
            assert any(len(text) > 0 for text in response_texts), "Response text is empty on mobile"
            
            print(f"✅ MOBILE: Response received successfully - {len(response_texts)} paragraph(s)")
            
        except Exception as e:
            print(f"❌ MOBILE: Error getting final response: {e}")
            response_texts = []
        
        return response_texts
