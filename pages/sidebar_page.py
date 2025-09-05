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
    HAMBURGER_BUTTON = (By.CSS_SELECTOR, "[data-testid='hamburger-button'], button[aria-haspopup='dialog'][data-state]")
    SIDEBAR = (By.CSS_SELECTOR, "[role='dialog'], .sidebar, .side-panel, .drawer, .sheet, [data-testid='sidebar']")
    NEW_CHAT_BUTTON = (By.CSS_SELECTOR, "button:has(svg[aria-label='New']), .new-chat, [aria-label='New chat']")
    SETTINGS_BUTTON = (By.CSS_SELECTOR, ".settings, [aria-label='Settings'], button[title*='Settings']")
    COLLAPSE_TOGGLE = (By.CSS_SELECTOR, "[aria-label*='Collapse'], [aria-label*='Expand']")
    CONVERSATION_ITEM_TITLES = (By.CSS_SELECTOR, ".conversation-item, .chat-item, [data-testid='conversation-item']")
    CLOSE_BUTTON = (By.XPATH, "//button[.//span[contains(@class,'sr-only') and normalize-space()='Close']]")
    # New reliable test IDs from app
    USER_MENU_BUTTON_STRICT = (By.XPATH, "//button[@data-testid='user-menu-button']")
    USER_MENU_BUTTON = (
        By.XPATH,
        "//body//*[contains(@class,'antialiased') and contains(@class,'tracking-tight') and contains(@class,'__className_')]//button[@aria-haspopup='menu']",
    )
    MENU_PULL_MODEL = (By.CSS_SELECTOR, "[data-testid='menu-pull-model']")
    MENU_SETTINGS = (By.CSS_SELECTOR, "[data-testid='menu-settings']")

    def __init__(self, driver):
        super().__init__(driver)
        print("Initialized Unified Sidebar Page")

    def open_sidebar_if_needed(self):
        """If on mobile and sidebar is closed, tap the hamburger to open it."""
        try:
            if self.is_mobile() and not self.is_element_present(self.SIDEBAR):
                assert self.is_element_present(self.HAMBURGER_BUTTON), "Hamburger button not found on mobile"
                self.click_hamburger()
                # Wait for either sidebar present OR button state open
                self._wait_sidebar_open_state()
        except Exception:
            pass
        return self

    def click_hamburger(self):
        """Explicitly click the hamburger button with robust interaction and fallback."""
        element = self.wait.until(EC.presence_of_element_located(self.HAMBURGER_BUTTON))
        try:
            self.wait.until(EC.element_to_be_clickable(self.HAMBURGER_BUTTON))
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});",
                element,
            )
            element.click()
        except Exception:
            # Fallback to JS click
            try:
                self.driver.execute_script("arguments[0].click();", element)
            except Exception:
                assert False, "Failed to click hamburger button"
        return self

    def _wait_sidebar_open_state(self, timeout: int = 10):
        """Wait until either the sidebar container appears or the button shows open state."""
        end_time = self.wait._timeout if hasattr(self.wait, "_timeout") else timeout
        try:
            self.wait.until(EC.presence_of_element_located(self.SIDEBAR))
            return True
        except Exception:
            pass
        # Check button state as alternative: data-state=open or aria-expanded=true
        try:
            self.wait.until(lambda d: (
                d.find_element(*self.HAMBURGER_BUTTON).get_attribute("data-state") == "open" or
                d.find_element(*self.HAMBURGER_BUTTON).get_attribute("aria-expanded") == "true"
            ))
            return True
        except Exception:
            assert False, "Sidebar did not open (no container and no open state on button)"

    def wait_for_load(self, timeout: int = 10):
        """Wait for the sidebar to be present (open first on mobile)."""
        self.open_sidebar_if_needed()
        try:
            self.wait.until(EC.presence_of_element_located(self.SIDEBAR))
        except TimeoutException:
            assert False, "Sidebar did not load within timeout"
        # Assert visible for debugging
        assert self.is_visible(), "Sidebar container is not visible after load"
        return self

    def wait_for_app_ready(self):
        """Wait for document.readyState to be complete before interacting."""
        self.wait.until(lambda d: d.execute_script('return document.readyState') == 'complete')
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
            assert self.is_element_present(self.COLLAPSE_TOGGLE), "Collapse/Expand toggle not found"
            self.click_element(self.COLLAPSE_TOGGLE)
        except TimeoutException:
            print("Collapse/Expand toggle not found")
        return self

    def open_new_chat(self):
        """Click the New Chat button in the sidebar."""
        self.open_sidebar_if_needed()
        try:
            assert self.is_element_present(self.NEW_CHAT_BUTTON), "New Chat button not present"
            self.click_element(self.NEW_CHAT_BUTTON)
        except TimeoutException:
            assert False, "New Chat button not found"
        return self

    def open_settings(self):
        """Open settings from the sidebar."""
        self.open_sidebar_if_needed()
        try:
            assert self.is_element_present(self.SETTINGS_BUTTON), "Settings button not present in sidebar"
            self.click_element(self.SETTINGS_BUTTON)
        except TimeoutException:
            print("Settings button not found in sidebar")
        return self

    def open_user_menu_by_name(self, name: str = "Anonymous"):
        """Deprecated: now uses data-testid to open the user menu, ignoring the name."""
        return self.open_user_menu()

    def open_user_menu(self):
        """Open the user menu using the reliable test id selector."""
        self.open_sidebar_if_needed()
        # Prefer strict data-testid selector if present
        locator = self.USER_MENU_BUTTON_STRICT if self.is_element_present(self.USER_MENU_BUTTON_STRICT) else self.USER_MENU_BUTTON
        assert self.is_element_present(locator), "User menu button not found"
        # Robust click similar to hamburger
        element = self.wait.until(EC.presence_of_element_located(locator))
        try:
            self.wait.until(EC.element_to_be_clickable(locator))
            self.driver.execute_script(
                "arguments[0].scrollIntoView({behavior: 'instant', block: 'center'});",
                element,
            )
            element.click()
        except Exception:
            try:
                self.driver.execute_script("arguments[0].click();", element)
            except Exception:
                assert False, "Failed to click user menu button"
        return self

    def open_settings_via_text(self):
        """Deprecated: use open_settings_from_menu (data-testid)."""
        return self.open_settings_from_menu()

    def open_settings_from_menu(self):
        """Open settings via the user menu item using data-testid. Returns SettingsPage."""
        from .settings_page import SettingsPage
        self.open_sidebar_if_needed()
        assert self.is_element_present(self.MENU_SETTINGS), "Menu 'Settings' item not found"
        self.click_element(self.MENU_SETTINGS)
        return SettingsPage(self.driver)

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
                    # Assert hidden
                    assert not self.is_element_present(self.SIDEBAR), "Sidebar still present after close"
                except TimeoutException:
                    print("Sidebar did not hide after clicking close")
        else:
            print("Close button not present")
        return self


