import pytest
import logging
from Tests.utils.browser_manager import get_driver
from Tests.UI.pages.login_page import LoginPage
from Tests.UI.pages.contact_list_page import ContactListPage


@pytest.fixture(scope="module")
def driver():
    driver_instance = get_driver()
    yield driver_instance
    driver_instance.quit()


def test_contact_list(driver):
    logger = logging.getLogger(__name__)
    logger.info("Starting test_contact_list...")

    login_page = LoginPage(driver)
    contact_list_page = ContactListPage(driver)

    logger.info("Logging in...")
    login_page.open()
    login_page.login()

    logger.info("Fetching contact list data...")
    contacts = contact_list_page.get_contacts()

    logger.info(f"Contacts retrieved: {contacts}")
    for contact in contacts:
        logger.info(f"Contact: {contact}")

    assert len(contacts) > 0, "Contact list is empty!"
    logger.info(f"Contact list test passed! Retrieved {len(contacts)} contacts.")
