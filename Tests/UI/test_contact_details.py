"""
    Test for Contact Details, Contact Edit pages
"""

import logging
from Tests.UI.pages.login_page import LoginPage
from Tests.UI.pages.contact_list_page import ContactListPage
from Tests.UI.pages.add_contact_page import AddContactPage
from Tests.UI.pages.contact_details import ContactDetailsPage
from Tests.UI.pages.contact_edit_page import ContactEditsPage
from Tests.config.user_creds import contact_details


def test_contact_details(driver):
    """
    tests for ContactDetail / ContactEdit pages
    """
    logger = logging.getLogger(__name__)
    login_page = LoginPage(driver)
    add_contact_page = AddContactPage(driver)
    contact_list_page = ContactListPage(driver)
    contact_detail_page = ContactDetailsPage(driver)
    contact_edit_page = ContactEditsPage(driver)

    logger.info("Logging in...")
    login_page.open()
    login_page.login()

    logger.info("Navigating to Add Contact page...")
    contact_list_page.click_add_contact()
    logger.info("Filling contact details...")
    add_contact_page.enter_contact_details(contact_details)
    logger.info("Submitting form...")
    add_contact_page.submit_form()

    logger.info("Collecting data from first row (first contact) in Contact List page...")
    contacts_list_single_collected = contact_list_page.get_contacts()
    logger.info("Navigating to Contact Details page...")
    contact_list_page.click_contact_data()
    logger.info("Collecting data from Contact Details page...")
    contact_detail_collected = contact_detail_page.collect_data()
    logger.info("Comparing data from Contact List page and Contact Details page...")
    list_and_detail_comparison1 = contact_detail_page.compare_dicts(
        contacts_list_single_collected[0], contact_detail_collected, ignore_keys={"id"}
    )
    assert list_and_detail_comparison1 is True
    logger.info("Navigating to Edit Contact page...")
    contact_detail_page.edit()
    logger.info("Updating contact details...")
    contact_edit_page.enter_contact_details(contact_details)
    logger.info("Submitting form...")
    contact_edit_page.submit_edit()
    logger.info("Collecting data from Contact Details page...")
    contact_detail_collected = contact_detail_page.collect_data()
    logger.info("Navigating to Contact List page...")
    contact_detail_page.return_to_list()
    logger.info("Collecting data from first row (first contact) in Contact List page...")
    contacts_list_single_collected = contact_list_page.get_contacts()
    logger.info("Comparing data from Contact List page and Contact Details page...")
    list_and_detail_comparison2 = (contact_detail_page.compare_dicts
        (contacts_list_single_collected[0],contact_detail_collected, ignore_keys={'id'})
    )
    assert list_and_detail_comparison2 is True
    logger.info("Navigating to Contact List page...")
    contact_list_page.click_contact_data()
    logger.info("Deleting contact data...")
    contact_detail_page.delete()
    logger.info("Checking Contact List page for ANY contacts...")
    no_contacts_in_list = contact_list_page.no_contacts()
    assert no_contacts_in_list
    logger.info("logging out...")
    contact_detail_page.logout()
