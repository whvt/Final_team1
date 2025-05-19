"""Tests for Contact details page"""

import logging
import time
import re
import pytest
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    StaleElementReferenceException,
)
from Tests.UI.pages.login_page import LoginPage
from Tests.UI.pages.contact_list_page import ContactListPage
from Tests.UI.pages.add_contact_page import AddContactPage
from Tests.UI.pages.contact_details import ContactDetailsPage
from Tests.UI.pages.contact_edit_page import ContactEditsPage
from Tests.config.user_creds import contact_details


def retry_step(retries=3, delay=1):
    """retry_step"""
    def decorator(func):
        def wrapper(*args, **kwargs):
            last_exc = None
            for _ in range(retries):
                try:
                    return func(*args, **kwargs)
                except (
                    TimeoutException,
                    NoSuchElementException,
                    StaleElementReferenceException,
                ) as e:
                    last_exc = e
                    time.sleep(delay)
            raise last_exc

        return wrapper

    return decorator


def test_contact_details(driver):
    """test contact details"""
    logger = logging.getLogger(__name__)
    log_in_page, add_contact_page = LoginPage(driver), AddContactPage(driver)
    contact_list_page, contact_detail_page = ContactListPage(driver), ContactDetailsPage(driver)
    contact_edit_page = ContactEditsPage(driver)
    logger.info("Logging in ...")
    log_in_page.open()
    log_in_page.login()
    logger.info("Navigating to Add Contact page ...")
    contact_list_page.click_add_contact()
    logger.info("Filling contact details ...")
    add_contact_page.enter_contact_details(contact_details)
    logger.info("Submitting form ...")
    add_contact_page.submit_form()
    logger.info(
        "Collecting data from first row (first contact) in Contact List page..."
    )
    contacts_list_single_collected = retry_step()(contact_list_page.get_contacts)()
    logger.info("Navigating to Contact Details page...")
    contact_list_page.click_contact_data()
    logger.info("Collecting data from Contact Details page...")
    contact_detail_collected = contact_detail_page.collect_data()
    logger.info("Comparing data from Contact List page and Contact Details page...")
    logger.info("Contact List data: %s", contacts_list_single_collected[0])
    logger.info("Contact Details data: %s", contact_detail_collected)

    try:
        if hasattr(contact_detail_page, "debug_page_elements"):
            contact_detail_page.debug_page_elements()
    except AttributeError as e:
        logger.warning("Failed to execute debug output: %s", str(e))

    list_and_detail_comparison1 = contact_detail_page.compare_dicts(
        contacts_list_single_collected[0], contact_detail_collected, ignore_keys={"id"}
    )
    assert list_and_detail_comparison1 is True
    logger.info("Navigating to Edit Contact page...")
    contact_detail_page.edit()
    logger.info("Updating contact details...")
    contact_edit_page.enter_contact_details(contact_details)
    contact_edit_page.submit_edit()
    contact_detail_collected = contact_detail_page.collect_data()
    logger.info("Navigating to Contact List page...")
    contact_detail_page.return_to_list()
    contacts_list_single_collected = retry_step()(contact_list_page.get_contacts)()
    logger.info("Comparing data from Contact List page and Contact Details page...")
    if contacts_list_single_collected:
        list_and_detail_comparison2 = contact_detail_page.compare_dicts(
            contacts_list_single_collected[-1],
            contact_detail_collected,
            ignore_keys={"id"},
        )
        assert list_and_detail_comparison2 is True
    logger.info("Navigating to Contact List page...")
    logger.info("Logging out...")
    contact_detail_page.logout()


@pytest.mark.demo
def test_contact_details_ui_elements(driver):
    """test contact details ui elements"""
    logger = logging.getLogger(__name__)
    log_in_page = LoginPage(driver)
    contact_list_page = ContactListPage(driver)
    contact_detail_page = ContactDetailsPage(driver)

    logger.info("Logging in...")
    log_in_page.open()
    log_in_page.login()

    contacts = retry_step()(contact_list_page.get_contacts)()
    if not contacts:
        logger.info("No contacts found, creating test contact...")
        add_contact_page = AddContactPage(driver)
        contact_list_page.click_add_contact()
        add_contact_page.enter_contact_details(contact_details)
        add_contact_page.submit_form()
        contact_list_page.click_contact_data()
    else:
        logger.info("Opening existing contact details page...")
        contact_list_page.click_contact_data()

    logger.info("Checking page header...")
    header_text = contact_detail_page.get_page_header()
    assert header_text == "Contact Details", f"Invalid page header: {header_text}"

    logger.info("Checking Edit and Return buttons presence...")
    assert contact_detail_page.is_edit_button_present(), (
        "Edit button is missing on the page"
    )
    assert contact_detail_page.is_return_button_present(), (
        "Return button is missing on the page"
    )

    logger.info("Logging out...")
    contact_detail_page.logout()


@pytest.mark.demo
def test_contact_details_field_presence(driver):
    """test contact details field presence"""
    logger = logging.getLogger(__name__)
    log_in_page = LoginPage(driver)
    contact_list_page = ContactListPage(driver)
    contact_detail_page = ContactDetailsPage(driver)

    logger.info("Logging in...")
    log_in_page.open()
    log_in_page.login()

    contacts = retry_step()(contact_list_page.get_contacts)()
    if not contacts:
        logger.info("No contacts found, creating test contact...")
        add_contact_page = AddContactPage(driver)
        contact_list_page.click_add_contact()
        add_contact_page.enter_contact_details(contact_details)
        add_contact_page.submit_form()
        contact_list_page.click_contact_data()
    else:
        logger.info("Opening existing contact details page...")
        contact_list_page.click_contact_data()

    logger.info("Checking presence of all required fields...")
    required_fields = ["firstName", "lastName", "birthdate", "email", "phone"]
    for field in required_fields:
        assert contact_detail_page.is_field_present(field), (
            f"Field {field} is missing on the page"
        )

    logger.info("Logging out...")
    contact_detail_page.logout()


def test_contact_details_non_empty_values(driver):
    """test contact details non empty values"""
    logger = logging.getLogger(__name__)
    log_in_page = LoginPage(driver)
    add_contact_page = AddContactPage(driver)
    contact_list_page = ContactListPage(driver)
    contact_detail_page = ContactDetailsPage(driver)

    logger.info("Logging in...")
    log_in_page.open()
    log_in_page.login()

    logger.info("Creating new contact...")
    contact_list_page.click_add_contact()
    add_contact_page.enter_contact_details(contact_details)
    add_contact_page.submit_form()

    logger.info("Waiting for contact list update...")
    time.sleep(1)

    contact_list_page.click_contact_data()

    logger.info("Waiting for contact details page to fully load...")
    time.sleep(2)

    contact_data = contact_detail_page.collect_data()

    logger.info("Collected contact data: %s", contact_data)

    logger.info("Checking non-empty values for fields...")
    required_non_empty_fields = ["name", "email", "phone"]
    for field in required_non_empty_fields:
        assert field in contact_data, f"Field {field} is missing in collected data"
        assert contact_data[field], f"Field {field} has empty value"

    logger.info("Deleting test contact and logging out...")
    contact_detail_page.delete()
    contact_detail_page.return_to_list()
    contact_detail_page.logout()


def test_contact_details_format_validation(driver):
    """test contact details format validation"""
    logger = logging.getLogger(__name__)
    log_in_page = LoginPage(driver)
    add_contact_page = AddContactPage(driver)
    contact_list_page = ContactListPage(driver)
    contact_detail_page = ContactDetailsPage(driver)

    logger.info("Logging in...")
    log_in_page.open()
    log_in_page.login()

    logger.info("Creating new contact...")
    contact_list_page.click_add_contact()

    test_contact = {
        "first_name": "Test",
        "last_name": "Format",
        "birthdate": "1990-01-01",
        "email": "test@example.com",
        "phone": "+1-234-567-8900",
        "street1": "123 Test St",
        "street2": "",
        "city": "TestCity",
        "state_province": "TS",
        "postal_code": "12345",
        "country": "TestCountry",
    }

    add_contact_page.enter_contact_details(test_contact)
    add_contact_page.submit_form()
    contact_list_page.click_contact_data()

    contact_data = contact_detail_page.collect_raw_data()

    if "birthdate" in contact_data and contact_data["birthdate"]:
        logger.info("Checking birthdate format...")
        date_pattern = r"^\d{4}-\d{2}-\d{2}$"
        assert re.match(date_pattern, contact_data["birthdate"]), (
            f"Invalid birthdate format: {contact_data['birthdate']}"
        )

    if "email" in contact_data and contact_data["email"]:
        logger.info("Checking email format...")
        assert "@" in contact_data["email"], (
            f"Email doesn't contain @ symbol: {contact_data['email']}"
        )
        assert "." in contact_data["email"].split("@")[1], (
            f"Email domain is invalid: {contact_data['email']}"
        )

    if "phone" in contact_data and contact_data["phone"]:
        logger.info("Checking phone format...")
        phone_pattern = r"^[0-9+\-() ]+$"
        assert re.match(phone_pattern, contact_data["phone"]), (
            f"Invalid phone format: {contact_data['phone']}"
        )

    logger.info("Deleting test contact and logging out...")
    contact_detail_page.delete()
    contact_detail_page.return_to_list()
    contact_detail_page.logout()
