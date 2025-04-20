import logging
import pytest
from Tests.utils.browser_manager import get_driver
from Tests.UI.pages.login_page import LoginPage


@pytest.fixture(scope="module")
def driver():
    driver_instance = get_driver()
    yield driver_instance
    driver_instance.quit()


def test_login(driver):
    logger = logging.getLogger(__name__)
    logger.info("Starting test_login...")

    login_page = LoginPage(driver)
    login_page.open()
    logger.info("Opening login page...")

    login_page.login()
    logger.info("Attempting to log in...")

    assert "Contact List" in driver.page_source, (
        "Login failed! 'Contact List' not found in page source."
    )
    logger.info("Login test passed!")
