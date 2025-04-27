"""
    Contact Details, Contact Edit pages
"""

import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Tests.UI.pages.base_page import BasePage


class ContactDetailsPage(BasePage):
    """
    Contact Details Page object
    """
    def __init__(self, driver):
        """
        ContactDetailsPage object init
        """
        super().__init__(driver)
        self.delete_contact_button = (By.ID, "delete")
        self.edit_contact_button = (By.ID, "edit-contact")
        self.return_to_list_button = (By.ID, "return")
        self.logout_button = ("id", "logout")
        self.edit_contact = (By.XPATH, "//h1[contains(text(), 'Edit Contact')]")
        self.contact_chart = (By.ID, "contactDetails")
        self.contact_chart_span = (By.TAG_NAME, "span")

    def logout(self):
        """
        click on logout button
        """
        self.wait_for_element(self.logout_button).click()

    def return_to_list(self):
        """
        click on contact list page
        """
        self.wait_for_element(self.return_to_list_button).click()

    def edit(self):
        """
        click on editing contact data
        """
        self.wait_for_element(self.edit_contact_button).click()

    def delete(self):
        """
        click on deleting button for in Contact Details page
        """
        self.wait_for_element(self.delete_contact_button).click()
        alert = self.driver.switch_to.alert
        alert.accept()

    def collect_data(self):
        """
        collecting data in Contact Details page
        """
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                self.contact_chart
            )
        )
        form = self.driver.find_element(*self.contact_chart)
        spans = form.find_elements(*self.contact_chart_span)
        contact_data = {}
        time.sleep(2)
        for span in spans:
            span_id = span.get_attribute("id")
            span_text = span.text.strip()
            if span_id:
                contact_data[span_id] = span_text
        contact_data['name'] = f"{contact_data.pop('firstName')} {contact_data.pop('lastName')}"
        if contact_data['street2'] != '':
            contact_data['address'] = f"{contact_data.pop('street1')} {contact_data.pop('street2')}"
        else:
            contact_data['address'] = f"{contact_data.pop('street1')}"
            contact_data.pop('street2')
        contact_data["location"] = (
            f"{contact_data.pop('city')} {contact_data.pop('stateProvince')} "
            f"{contact_data.pop('postalCode')}"
        )
        return contact_data

    @staticmethod
    def compare_dicts(dict1, dict2, ignore_keys=None):
        """
        comparing data in Contact Details and Contact List pages
        """
        if ignore_keys is None:
            ignore_keys = set()
        dict1_filtered = {k: v for k, v in dict1.items() if k not in ignore_keys}
        dict2_filtered = {k: v for k, v in dict2.items() if k not in ignore_keys}
        keys1 = set(dict1_filtered.keys())
        keys2 = set(dict2_filtered.keys())
        common_keys = keys1 & keys2
        only_in_dict1 = keys1 - keys2
        only_in_dict2 = keys2 - keys1
        value_differences = {}
        for key in common_keys:
            if dict1_filtered[key] != dict2_filtered[key]:
                value_differences[key] = (dict1_filtered[key], dict2_filtered[key])
        identical = not (only_in_dict1 or only_in_dict2 or value_differences)
        if not identical:
            if value_differences:
                print("Обнаружены различия. Различия в значениях:")
                for key, (val1, val2) in value_differences.items():
                    print(f" {key}: {val1} (first) != {val2} (second)", 'len1=|',
                          len(val1), 'len2=|', len(val2))
        return identical
