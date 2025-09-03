"""Unified Sidebar Page with a shared API for all devices"""

import sys
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from .base_page import BasePage


class SidebarPage(BasePage):
    """Single sidebar page that handles minor mobile/desktop differences internally."""

    # Common locators (kept broad to be resilient)
    HAMBURGER_BUTTON = (By.CSS_SELECTOR, "button[aria-haspopup='dialog'][data-state]")
    SIDEBAR = (By.CSS_SELECTOR, ".sidebar, .side-panel, .drawer, .sheet, [data-testid='sidebar']")
    NEW_CHAT_BUTTON = (By.CSS_SELECTOR, "button:has(svg[aria-label='New']), .new-chat, [aria-label='New chat']")
    SETTINGS_BUTTON = (By.CSS_SELECTOR, ".settings, [aria-label='Settings'], button[title*='Settings']")
    COLLAPSE_TOGGLE = (By.CSS_SELECTOR, "[aria-label*='Collapse'], [aria-label*='Expand']")
    CONVERSATION_ITEM_TITLES = (By.CSS_SELECTOR, ".conversation-item, .chat-item, [data-testid='conversation-item']")
    CLOSE_BUTTON = (By.XPATH, "//button[.//span[contains(@class,'sr-only') and normalize-space()='Close']]")

    def __init__(self, driver):
        super().__init__(driver)
        print("Initialized Unified Sidebar Page")

    def open_sidebar_if_needed(self):
        """If on mobile and sidebar is closed, tap the hamburger to open it."""
        try:
            if self.is_mobile() and not self.is_element_present(self.SIDEBAR):
                if self.is_element_present(self.HAMBURGER_BUTTON):
                    self.click_element(self.HAMBURGER_BUTTON)
        except Exception:
            pass
        return self

    def wait_for_load(self, timeout: int = 10):
        """Wait for the sidebar to be present (open first on mobile)."""
        self.open_sidebar_if_needed()
        try:
            self.wait.until(EC.presence_of_element_located(self.SIDEBAR))
        except TimeoutException:
            assert False, "Sidebar did not load within timeout"
        return self

    def is_visible(self) -> bool:
        """Check if sidebar is present and displayed."""
        try:
            element = self.wait.until(EC.presence_of_element_located(self.SIDEBAR))
            return element.is_displayed()
        except TimeoutException:
            return False

    def toggle_collapse(self):
        """Toggle sidebar collapse/expand if toggle exists (desktop layouts)."""
        try:
            self.click_element(self.COLLAPSE_TOGGLE)
        except TimeoutException:
            print("Collapse/Expand toggle not found")
        return self

    def open_new_chat(self):
        """Click the New Chat button in the sidebar."""
        self.open_sidebar_if_needed()
        try:
            self.click_element(self.NEW_CHAT_BUTTON)
        except TimeoutException:
            assert False, "New Chat button not found"
        return self

    def open_settings(self):
        """Open settings from the sidebar."""
        self.open_sidebar_if_needed()
        try:
            self.click_element(self.SETTINGS_BUTTON)
        except TimeoutException:
            print("Settings button not found in sidebar")
        return self

    def select_conversation(self, title_substring: str):
        """Select a conversation by partial title match."""
        self.open_sidebar_if_needed()
        items = self.driver.find_elements(*self.CONVERSATION_ITEM_TITLES)
        for item in items:
            try:
                text = (item.text or "").strip()
                if title_substring.lower() in text.lower():
                    item.click()
                    return self
            except Exception:
                continue
        assert False, f"Conversation containing '{title_substring}' not found"

    def close_sidebar(self, wait_until_hidden: bool = True, timeout: int = 10):
        """Click the sidebar close button (if present) and optionally wait until it hides."""
        if self.is_element_present(self.CLOSE_BUTTON):
            self.click_element(self.CLOSE_BUTTON)
            if wait_until_hidden:
                try:
                    self.wait.until(EC.invisibility_of_element_located(self.SIDEBAR))
                except TimeoutException:
                    print("Sidebar did not hide after clicking close")
        else:
            print("Close button not present")
        return self


