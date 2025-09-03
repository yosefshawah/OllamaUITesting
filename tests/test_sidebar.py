import pytest
from pages.page_factory import PageFactory


@pytest.fixture
def mobile_driver(driver):
    """Force mobile viewport for this test (width < 1024)."""
    driver.set_window_size(800, 900)
    return driver


def test_sidebar_hamburger_click(mobile_driver, base_url):
    """Open the app, click hamburger on mobile to open sidebar, and verify sidebar is visible.
    On desktop, sidebar should already be visible and the test still passes.
    """
    driver = mobile_driver
    driver.get(base_url)

    sidebar = PageFactory.create_sidebar_page(driver)

    if sidebar.is_mobile():
        # If sidebar is not present, click the hamburger and wait for it
        if not sidebar.is_element_present(sidebar.SIDEBAR):
            sidebar.click_element(sidebar.HAMBURGER_BUTTON)
        # Wait for sidebar to be present/visible
        sidebar.wait_for_load()
        assert sidebar.is_visible(), "Sidebar should be visible after clicking hamburger on mobile"
        # Close the sidebar and finish gracefully
        sidebar.close_sidebar()
    else:
        # Desktop: sidebar should already be available
        sidebar.wait_for_load()
        assert sidebar.is_visible(), "Sidebar should be visible on desktop layouts"


