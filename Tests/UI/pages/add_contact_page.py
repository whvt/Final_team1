from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from Tests.UI.pages.base_page import BasePage


class AddContactPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.logout_button = ("id", "logout")
        self.error_message = ("id", "error")
        self.first_name_input = ("id", "firstName")
        self.last_name_input = ("id", "lastName")
        self.birthdate_input = ("id", "birthdate")
        self.email_input = ("id", "email")
        self.phone_input = ("id", "phone")
        self.street1_input = ("id", "street1")
        self.street2_input = ("id", "street2")
        self.city_input = ("id", "city")
        self.state_province_input = ("id", "stateProvince")
        self.postal_code_input = ("id", "postalCode")
        self.country_input = ("id", "country")
        self.submit_button = ("id", "submit")
        self.cancel_button = ("id", "cancel")

    def logout(self):
        self.wait_for_element(self.logout_button).click()

    def enter_contact_details(self, contact_details):
        self.wait_for_element(self.first_name_input).send_keys(
            contact_details["first_name"]
        )
        self.wait_for_element(self.last_name_input).send_keys(
            contact_details["last_name"]
        )
        self.wait_for_element(self.birthdate_input).send_keys(
            contact_details["birthdate"]
        )
        self.wait_for_element(self.email_input).send_keys(contact_details["email"])
        self.wait_for_element(self.phone_input).send_keys(contact_details["phone"])
        self.wait_for_element(self.street1_input).send_keys(contact_details["street1"])
        self.wait_for_element(self.street2_input).send_keys(contact_details["street2"])
        self.wait_for_element(self.city_input).send_keys(contact_details["city"])
        self.wait_for_element(self.state_province_input).send_keys(
            contact_details["state_province"]
        )
        self.wait_for_element(self.postal_code_input).send_keys(
            contact_details["postal_code"]
        )
        self.wait_for_element(self.country_input).send_keys(contact_details["country"])

    def submit_form(self):
        self.wait_for_element(self.submit_button).click()

        error_message = self.get_error_message()
        if error_message:
            print(f"Form submission error: {error_message}")

        WebDriverWait(self.driver, 10).until(EC.url_contains("contactList"))

    def cancel_form(self):
        self.wait_for_element(self.cancel_button).click()

    def get_error_message(self):
        error_element = self.wait_for_element(self.error_message)
        return error_element.text if error_element else None
