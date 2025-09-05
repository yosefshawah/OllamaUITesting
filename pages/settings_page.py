from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage


class SettingsPage(BasePage):
    NAME_INPUT = (By.CSS_SELECTOR, "input[placeholder='Enter your name']")
    CHANGE_NAME_BUTTON = (By.XPATH, "//button[@type='submit' and normalize-space()='Change name']")
    THEME_LIGHT_BUTTON = (By.XPATH, "//button[.//p[normalize-space()='Light']]")

    def wait_for_load(self):
        self.wait.until(EC.presence_of_element_located(self.NAME_INPUT))
        assert self.is_element_present(self.NAME_INPUT), "Name input not present on Settings page"
        return self

    def enter_name(self, name: str):
        assert name, "Name must be a non-empty string"
        self.enter_text(self.NAME_INPUT, name)
        # Verify text entered
        element = self.wait.until(EC.presence_of_element_located(self.NAME_INPUT))
        value = element.get_attribute("value") or element.text
        assert name in (value or ""), f"Expected name '{name}' to be entered, got '{value}'"
        return self

    def submit_change_name(self):
        assert self.is_element_present(self.CHANGE_NAME_BUTTON), "Change name button not present"
        self.click_element(self.CHANGE_NAME_BUTTON)
        return self

    def select_light_theme(self):
        """Click the Light theme option (button containing a p tag with text 'Light')."""
        assert self.is_element_present(self.THEME_LIGHT_BUTTON), "Light theme button not present"
        self.click_element(self.THEME_LIGHT_BUTTON)
        # Wait for the html style color-scheme to reflect 'light'
        self.wait.until(lambda d: (d.find_element(By.TAG_NAME, 'html').get_attribute('style') or '').lower().find('color-scheme: light') != -1)
        return self

    def assert_html_color_scheme(self, expected: str):
        """Assert that the html tag's inline style has color-scheme equal to expected (case-insensitive)."""
        html_style = (self.driver.find_element(By.TAG_NAME, 'html').get_attribute('style') or '').strip()
        assert f"color-scheme: {expected.lower()}" in html_style.lower(), f"Expected html style to contain 'color-scheme: {expected}', got: {html_style}"
        return self

