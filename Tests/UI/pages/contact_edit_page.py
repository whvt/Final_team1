"""
    Contact Edit pages
"""
from selenium.webdriver.common.by import By
from Tests.UI.pages.base_page import BasePage


class ContactEditsPage(BasePage):
    """
    Contact Edit Page object
    """
    def __init__(self, driver):
        """
        ContactEditsPage object init
        """
        super().__init__(driver)
        self.submit = (By.ID, "submit")
        self.first_name_input = (By.ID, "firstName")
        self.last_name_input = (By.ID, "lastName")
        self.birthdate_input = (By.ID, "birthdate")
        self.email_input = (By.ID, "email")
        self.phone_input = (By.ID, "phone")
        self.address1_input = (By.ID, "street1")
        self.address2_input = (By.ID, "street2")
        self.city_input = (By.ID, "city")
        self.state_input = (By.ID, "stateProvince")
        self.postal_code_input = (By.ID, "postalCode")
        self.country_input = (By.ID, "country")

    def enter_contact_details(self, contact_details):
        """
        updating contact data
        """
        self.wait_for_element(self.email_input).clear()
        self.wait_for_element(self.email_input).send_keys(contact_details["email2"])
        self.wait_for_element(self.phone_input).clear()
        self.wait_for_element(self.phone_input).send_keys(contact_details["phone2"])
        self.wait_for_element(self.address1_input).clear()
        self.wait_for_element(self.address1_input).send_keys(contact_details["street1-2"])
        self.wait_for_element(self.address2_input).clear()
        self.wait_for_element(self.address2_input).send_keys(contact_details["street2-2"])
        self.wait_for_element(self.city_input).clear()
        self.wait_for_element(self.city_input).send_keys(contact_details["city2"])
        self.wait_for_element(self.state_input).clear()
        self.wait_for_element(self.state_input).send_keys(
            contact_details["state_province2"]
        )
        self.wait_for_element(self.postal_code_input).clear()
        self.wait_for_element(self.postal_code_input).send_keys(
            contact_details["postal_code2"]
        )
        self.wait_for_element(self.country_input).clear()
        self.wait_for_element(self.country_input).send_keys(contact_details["country2"])
        self.wait_for_element(self.first_name_input).clear()
        self.wait_for_element(self.first_name_input).send_keys(contact_details["first_name2"])
        self.wait_for_element(self.last_name_input).clear()
        self.wait_for_element(self.last_name_input).send_keys(contact_details["last_name2"])
        self.wait_for_element(self.birthdate_input).clear()
        self.wait_for_element(self.birthdate_input).send_keys(contact_details["birthdate2"])

    def submit_edit(self):
        """
        click submit button
        """
        self.wait_for_element(self.submit).click()
