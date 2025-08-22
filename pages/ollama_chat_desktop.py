"""Desktop-specific implementation of Ollama Chat Page"""

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from time import sleep
from .base_page import BasePage

class OllamaChatDesktopPage(BasePage):
    """Desktop-specific chat page with desktop UI patterns"""
    
    # Desktop-specific locators
    SELECT_MODEL_BUTTON = (By.XPATH, "//button[normalize-space(text())='Select model']")
    MODEL_DIALOG = (By.XPATH, '//div[@role="dialog"]')
    FIRST_MODEL_BUTTON = (By.XPATH, '//div[@role="dialog"]//button')
    PROMPT_INPUT = (By.CSS_SELECTOR, '[placeholder="Enter your prompt here"]')
    SUBMIT_BUTTON = (By.CSS_SELECTOR, 'button[type="submit"]')
    OLLAMA_IMG = (By.XPATH, "//img[@src='/ollama.png']")
    
    # Desktop-specific UI elements
    SIDEBAR = (By.CSS_SELECTOR, '.sidebar, .navigation, .side-panel')
    MAIN_CONTENT = (By.CSS_SELECTOR, '.main-content, .chat-area, .conversation-area')
    SETTINGS_BUTTON = (By.CSS_SELECTOR, '.settings, [aria-label="Settings"]')
    
    def __init__(self, driver):
        super().__init__(driver)
        print("Initialized Desktop Chat Page")
    
    def navigate_to(self, url):
        """Navigate to the Ollama chat page"""
        print(f"🖥️ DESKTOP: Navigating to {url}")
        self.driver.get(url)
        
        # Assert page loaded successfully
        current_url = self.driver.current_url
        assert url in current_url, f"Failed to navigate to {url}. Current URL: {current_url}"
        print(f"✅ DESKTOP: Successfully navigated to {current_url}")
        
        # Assert basic page structure exists
        page_title = self.driver.title
        assert page_title, "Page title is empty - page may not have loaded properly"
        print(f"✅ DESKTOP: Page loaded with title: '{page_title}'")
        
        return self
    
    def clear_app_state(self):
        """Clear browser storage and refresh page"""
        print("🖥️ DESKTOP: Clearing application state")
        
        try:
            self.driver.execute_script(
                "try { localStorage.clear(); } catch (e) { console.log('localStorage not available'); }"
                "try { sessionStorage.clear(); } catch (e) { console.log('sessionStorage not available'); }"
                "try { indexedDB.databases().then(dbs => dbs.forEach(db => indexedDB.deleteDatabase(db.name))); } catch (e) { console.log('indexedDB not available'); }"
            )
            print("✅ DESKTOP: Browser storage cleared successfully")
        except Exception as e:
            print(f"⚠️ DESKTOP: Warning - Could not clear browser storage: {e}")
        
        print("🖥️ DESKTOP: Refreshing page")
        self.driver.refresh()
        
        # Wait for page to be fully loaded
        self.wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
        
        # Assert page refreshed properly
        current_url = self.driver.current_url
        assert current_url, "Current URL is empty after refresh"
        print(f"✅ DESKTOP: Page refreshed successfully - URL: {current_url}")
        
        return self
    
    def wait_for_sidebar_load(self):
        """Wait for sidebar to load (desktop-specific)"""
        try:
            self.wait.until(EC.presence_of_element_located(self.SIDEBAR))
        except TimeoutException:
            print("Sidebar not found - might be a different layout")
        return self
    
    def select_model(self):
        """Desktop-specific model selection flow"""
        print("🖥️ DESKTOP: Starting model selection")
        
        # Assert select model button exists
        assert self.is_element_present(self.SELECT_MODEL_BUTTON), "Select model button not found on desktop"
        print("✅ DESKTOP: Select model button found")
        
        # Click the "Select model" button
        self.click_element(self.SELECT_MODEL_BUTTON)
        
        # Assert dialog appeared
        assert self.is_element_present(self.MODEL_DIALOG), "Model selection dialog not found on desktop"
        print("✅ DESKTOP: Model selection dialog opened")
        
        # Assert first model button exists
        assert self.is_element_present(self.FIRST_MODEL_BUTTON), "First model button not found in desktop dialog"
        print("✅ DESKTOP: First model button found")
        
        # Wait for dialog to appear and click first model
        self.click_element(self.FIRST_MODEL_BUTTON)
        print("✅ DESKTOP: Model selected successfully")
        
        return self
    
    def enter_prompt(self, text):
        """Enter text in the desktop prompt input"""
        print(f"🖥️ DESKTOP: Entering prompt text: '{text}'")
        
        # Assert prompt input exists
        assert self.is_element_present(self.PROMPT_INPUT), "Prompt input field not found on desktop"
        print("✅ DESKTOP: Prompt input field found")
        
        self.enter_text(self.PROMPT_INPUT, text)
        
        # Assert text was entered correctly
        entered_text = self.get_prompt_value()
        assert text in entered_text, f"Text not entered correctly. Expected: '{text}', Found: '{entered_text}'"
        print(f"✅ DESKTOP: Text entered successfully: '{entered_text}'")
        
        return self
    
    def get_prompt_value(self):
        """Get the current value of the prompt input"""
        element = self.wait.until(EC.presence_of_element_located(self.PROMPT_INPUT))
        return element.get_attribute("value")
    
    def submit_prompt(self):
        """Submit prompt with desktop-optimized interaction"""
        print("🖥️ DESKTOP: Submitting prompt")
        
        # Assert submit button exists
        assert self.is_element_present(self.SUBMIT_BUTTON), "Submit button not found on desktop"
        print("✅ DESKTOP: Submit button found")
        
        submit_button = self.wait.until(EC.presence_of_element_located(self.SUBMIT_BUTTON))
        
        # Wait for button to be enabled
        self.wait.until(lambda d: submit_button.is_enabled())
        assert submit_button.is_enabled(), "Submit button is not enabled on desktop"
        print("✅ DESKTOP: Submit button is enabled")
        
        # Desktop can use instant scrolling
        self.driver.execute_script(
            "arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});", 
            submit_button
        )
        print("✅ DESKTOP: Scrolled to submit button")
        
        # Wait for button to be clickable after scrolling
        self.wait.until(EC.element_to_be_clickable(self.SUBMIT_BUTTON)).click()
        print("✅ DESKTOP: Prompt submitted successfully")
        
        return self
    
    def wait_for_response(self, timeout=20):
        """Wait for AI response on desktop"""
        print("🖥️ DESKTOP: Waiting for AI response")
        response_wait = WebDriverWait(self.driver, timeout)
        
        # Wait for ollama.png image to appear
        try:
            ollama_img = response_wait.until(
                EC.presence_of_element_located(self.OLLAMA_IMG)
            )
            print("✅ DESKTOP: Found ollama.png image - response started")
        except Exception as e:
            assert False, f"Ollama response image not found on desktop within {timeout}s: {e}"
        
        # Desktop-specific response detection
        response_xpath = "//img[@src='/ollama.png']/ancestor::div[1]//p | //img[@src='/ollama.png']/following-sibling::*/descendant-or-self::p"
        
        # Wait for response text to stabilize
        print("🖥️ DESKTOP: Waiting for response text to stabilize")
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
                print(f"⚠️ DESKTOP: Error finding response: {e}")
            
            max_attempts -= 1
            sleep(0.5)
        
        # Get final response
        try:
            response_paragraphs = self.driver.find_elements(By.XPATH, response_xpath)
            response_texts = [p.text.strip() for p in response_paragraphs if p.text.strip()]
            
            # Assert we got a response
            assert len(response_texts) > 0, "No response text found on desktop"
            assert any(len(text) > 0 for text in response_texts), "Response text is empty on desktop"
            
            print(f"✅ DESKTOP: Response received successfully - {len(response_texts)} paragraph(s)")
            
        except Exception as e:
            print(f"❌ DESKTOP: Error getting final response: {e}")
            response_texts = []
        
        return response_texts
    
    def access_settings(self):
        """Access settings menu (desktop-specific)"""
        try:
            self.click_element(self.SETTINGS_BUTTON)
            return self
        except TimeoutException:
            print("Settings button not found")
            return self
    
    def check_sidebar_presence(self):
        """Check if sidebar is present (desktop layout indicator)"""
        return self.is_element_present(self.SIDEBAR)
