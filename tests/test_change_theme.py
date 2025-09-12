import os
import sys
import unittest

# Ensure project root for direct debug runs
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from utils.driver_factory import DriverFactory
from pages.page_factory import PageFactory
from utils.allure_decorators import allure_matrix, severity_level


class TestChangeTheme(unittest.TestCase):
    def setUp(self):
        self.driver = DriverFactory.create_driver(headless=False)
        self.base_url = os.getenv('OLLAMA_URL', 'http://localhost:3000')

    def tearDown(self):
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()

    @allure_matrix(
        title=lambda: "Change theme to Light",
        description=lambda: "Open user menu, go to settings, set theme to Light, assert color-scheme.",
        severity=severity_level.CRITICAL,
        owner="UI Team",
        link=("https://dev.example.com/", "Website"),
        issue=lambda: os.getenv('ALLURE_ISSUE', 'UI-CHANGE-THEME'),
        testcase=lambda: os.getenv('ALLURE_TMS', 'TMS-CHANGE-THEME'),
    )
    def test_select_light_theme_and_assert(self):
        """Open app, navigate to settings, choose Light theme, then assert color-scheme."""
        self.driver.get(self.base_url)
        (
            PageFactory.create_sidebar_page(self.driver)
                .wait_for_app_ready()
                .open_user_menu()
                .open_settings_from_menu()
                .wait_for_load()
                .select_light_theme()
                .assert_html_color_scheme("light")
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)


