""""Tests for Contact list page"""


import logging
from Tests.UI.pages.login_page import LoginPage
from Tests.UI.pages.contact_list_page import ContactListPage


def test_contact_list(driver):
    """test contact list"""
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


def test_contact_list_table_structure(driver):
    """test contact list table structure"""
    logger = logging.getLogger(__name__)
    logger.info("Starting test_contact_list...")
    login_page = LoginPage(driver)
    contact_list_page = ContactListPage(driver)
    logger.info("Logging in...")
    login_page.open()
    login_page.login()
    logger.info("Checking contact list table structure...")
    contacts_table_structure = contact_list_page.contact_list_table_structure()
    assert contacts_table_structure is True, "Contact list table isn't correct!"
    contacts_table_header = contact_list_page.contact_list_table_header()
    assert len(contacts_table_header) == 7
    assert contacts_table_header[0].text == "Name"
    assert contacts_table_header[1].text == "Birthdate"
    assert contacts_table_header[2].text == "Email"
    assert contacts_table_header[3].text == "Phone"
    assert contacts_table_header[4].text == "Address"
    assert contacts_table_header[5].text == "City, State/Province, Postal Code"
    assert contacts_table_header[6].text == "Country"
    logger.info("Contact table structure is correct!.")


def test_contact_list_table_duplicates(driver):
    """test duplicate exists in contact list table"""
    logger = logging.getLogger(__name__)
    logger.info("Starting test_contact_list...")
    login_page = LoginPage(driver)
    contact_list_page = ContactListPage(driver)
    logger.info("Logging in...")
    login_page.open()
    login_page.login()
    logger.info("looking for duplicates...")
    duplicates = contact_list_page.contact_list_table_duplicates()
    assert len(duplicates) > 0, "Не найдены полные дубликаты контактов"
    logger.info("Duplicates were found, quantity is : %s.", duplicates)


def test_add_contact_button(driver):
    """test add contact button functionality"""
    logger = logging.getLogger(__name__)
    logger.info("Starting test_contact_list...")
    login_page = LoginPage(driver)
    contact_list_page = ContactListPage(driver)
    logger.info("Logging in...")
    login_page.open()
    login_page.login()
    logger.info("Checking add contact button...")
    contact_list_page.click_add_contact()
    assert "Add Contact" in driver.title


def test_logout_functionality(driver):
    """test logout button functionality"""
    logger = logging.getLogger(__name__)
    logger.info("Starting test_contact_list...")
    login_page = LoginPage(driver)
    contact_list_page = ContactListPage(driver)
    logger.info("Logging in...")
    login_page.open()
    login_page.login()
    logger.info("Checking logging out button...")
    contact_list_page.logout()
    assert "Contact List App" in driver.title
