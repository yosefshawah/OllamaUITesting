from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from .base_page import BasePage


class SettingsPage(BasePage):
    NAME_INPUT = (By.CSS_SELECTOR, "input[placeholder='Enter your name']")
    CHANGE_NAME_BUTTON = (By.XPATH, "//button[@type='submit' and normalize-space()='Change name']")

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

