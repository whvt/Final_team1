import logging
from Tests.UI.pages.login_page import LoginPage
from Tests.UI.pages.contact_list_page import ContactListPage
from Tests.UI.pages.add_contact_page import AddContactPage
from Tests.config.user_creds import contact_details


def test_add_contact(driver):
    logger = logging.getLogger(__name__)
    logger.info("Starting test_add_contact...")

    login_page = LoginPage(driver)
    contact_list_page = ContactListPage(driver)
    add_contact_page = AddContactPage(driver)

    logger.info("Logging in...")
    login_page.open()
    login_page.login()

    logger.info("Navigating to Add Contact page...")
    contact_list_page.click_add_contact()

    logger.info("Filling contact details...")
    add_contact_page.enter_contact_details(contact_details)

    logger.info("Submitting form...")
    add_contact_page.submit_form()

    logger.info("Checking if redirected to Contact List page...")
    assert "contactList" in driver.current_url, (
        "Failed to redirect to Contact List page after form submission!"
    )

    logger.info("Fetching updated contact list...")
    contacts = contact_list_page.get_contacts()

    logger.info("Contacts after addition: %s", contacts)

    assert any(
        contact["name"] == "Alice Smith"
        and contact["email"] == "alice.smith@example.com"
        for contact in contacts
    ), "New contact not found in contact list!"
    logger.info("Add Contact test passed!")
