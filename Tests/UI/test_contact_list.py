import logging

from Tests.UI.pages.login_page import LoginPage
from Tests.UI.pages.contact_list_page import ContactListPage


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

    logger.info("Contacts retrieved: %s", contacts)
    for contact in contacts:
        logger.info("Contact: %s", contact)

    assert len(contacts) > 0, "Contact list is empty!"
    logger.info("Contact list test passed! Retrieved %s contacts.", len(contacts))
