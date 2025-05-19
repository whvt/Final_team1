"""Contact details page"""

import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.common.exceptions import (
    NoSuchElementException,
    StaleElementReferenceException,
    TimeoutException,
)
from Tests.UI.pages.base_page import BasePage


# def smart_wait_retry(func, retries=3, delay=1, *args, **kwargs):
def smart_wait_retry(func, *args, retries=3, delay=1, **kwargs):
    """smart wait retry"""
    last_exc = None
    for _ in range(retries):
        try:
            return func(*args, **kwargs)
        except (TimeoutException, NoSuchElementException, StaleElementReferenceException) as e:
            last_exc = e
            time.sleep(delay)
    raise last_exc


class ContactDetailsPage(BasePage):
    """Contact Details Page class"""
    def __init__(self, driver):
        """init"""
        super().__init__(driver)
        self.delete_contact_button = (By.ID, "delete")
        self.edit_contact_button = (By.ID, "edit-contact")
        self.return_to_list_button = (By.ID, "return")
        self.logout_button = ("id", "logout")
        self.edit_contact = (By.XPATH, "//h1[contains(text(), 'Edit Contact')]")
        self.contact_chart = (By.ID, "contactDetails")
        self.contact_chart_span = (By.TAG_NAME, "span")

    def logout(self):
        """logout"""
        smart_wait_retry(lambda: self.wait_for_element(self.logout_button).click())

    def return_to_list(self):
        """return to list"""
        smart_wait_retry(lambda: self.wait_for_element(self.return_to_list_button).click())

    def edit(self):
        """edit"""
        smart_wait_retry(lambda: self.wait_for_element(self.edit_contact_button).click())

    def delete(self):
        """delete"""
        smart_wait_retry(self.wait_for_element(self.delete_contact_button).click)
        smart_wait_retry(self.driver.switch_to.alert.accept)

    def collect_data(self):
        """collect data"""

        def _collect():
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.contact_chart)
            )
            time.sleep(0.5)
            form = self.driver.find_element(*self.contact_chart)
            WebDriverWait(self.driver, 5).until(EC.visibility_of(form))
            spans = form.find_elements(*self.contact_chart_span)
            WebDriverWait(self.driver, 5).until(lambda d: len(spans) > 0)
            contact_data = {}
            for span in spans:
                span_id = span.get_attribute("id")
                span_text = span.text.strip()
                if span_id:
                    if not span_text:
                        try:
                            # Фиксируем span_id через аргумент по умолчанию
                            WebDriverWait(self.driver, 3).until(
                                lambda d, span_id=span_id: d.find_element(
                                    By.ID, span_id
                                ).text.strip()
                                != ""
                            )
                            span_text = self.driver.find_element(
                                By.ID, span_id
                            ).text.strip()
                        except TimeoutException:
                            pass
                    contact_data[span_id] = span_text
            first_name = contact_data.get("firstName", "").strip()
            last_name = contact_data.get("lastName", "").strip()
            contact_data["name"] = f"{first_name} {last_name}".strip()
            street1 = contact_data.get("street1", "").strip()
            if street2 := contact_data.get("street2", "").strip():
                contact_data["address"] = f"{street1} {street2}".strip()
            else:
                contact_data["address"] = street1
            contact_data.pop("firstName", None)
            contact_data.pop("lastName", None)
            contact_data.pop("street1", None)
            contact_data.pop("street2", None)
            city = contact_data.get("city", "").strip()
            state = contact_data.get("stateProvince", "").strip()
            postal = contact_data.get("postalCode", "").strip()
            contact_data["location"] = f"{city} {state} {postal}".strip()
            contact_data.pop("city", None)
            contact_data.pop("stateProvince", None)
            contact_data.pop("postalCode", None)
            for key in ["email", "phone", "country", "birthdate"]:
                contact_data[key] = contact_data.get(key, "").strip()
            return contact_data
        return smart_wait_retry(_collect)

    @staticmethod
    def compare_dicts(dict1, dict2, ignore_keys=None):
        """compare dicts"""
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
                print("Differences found. Value differences:")
                for key, (val1, val2) in value_differences.items():
                    print(f" {key}: {val1} (first) != {val2} (second)", 'len1=|',
                          len(val1), 'len2=|', len(val2))
        return identical

    def get_page_header(self):
        """get page header"""
        header_locator = (By.TAG_NAME, "h1")
        return smart_wait_retry(lambda: self.wait_for_element(header_locator).text)

    def is_edit_button_present(self):
        """is edit button present"""
        try:
            return smart_wait_retry(
                lambda: self.wait_for_element(self.edit_contact_button, timeout=5)
                        is not None
            )
        except NoSuchElementException:
            return False

    def is_return_button_present(self):
        """is return button present"""
        try:
            return smart_wait_retry(
                lambda: self.wait_for_element(self.return_to_list_button, timeout=5)
                        is not None
            )
        except NoSuchElementException:
            return False

    def is_field_present(self, field_id):
        """is field button present"""
        field_locator = (By.ID, field_id)
        try:
            return smart_wait_retry(
                lambda: self.wait_for_element(field_locator, timeout=5) is not None
            )
        except NoSuchElementException:
            return False

    def debug_page_elements(self):
        """debug page elements"""
        try:
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.contact_chart)
            )
            form = self.driver.find_element(*self.contact_chart)
            spans = form.find_elements(*self.contact_chart_span)

            print(f"Found {len(spans)} span elements")

            for i, span in enumerate(spans):
                span_id = span.get_attribute("id") or "No ID"
                span_text = span.text.strip() or "No text"
                span_class = span.get_attribute("class") or "No class"
                print(f"Span #{i}: ID={span_id}, Text='{span_text}', Class={span_class}")

            return True
        except TimeoutException:
            print("Timeout: Contact chart element not found within 10 seconds")
            return False
        except NoSuchElementException as e:
            print(f"Element not found: {str(e)}")
            return False

    def collect_raw_data(self):
        """Collect raw contact data from the contact chart"""

        def _collect():
            """Collect contact data from visible spans"""
            WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located(self.contact_chart)
            )
            time.sleep(0.5)  # Small delay for stability
            form = self.driver.find_element(*self.contact_chart)
            WebDriverWait(self.driver, 5).until(
                EC.visibility_of(form)
            )
            spans = form.find_elements(*self.contact_chart_span)
            WebDriverWait(self.driver, 5).until(
                lambda d: len(d.find_elements(*self.contact_chart_span)) > 0
            )
            contact_data = {}
            for span in spans:
                current_span = span
                span_id = current_span.get_attribute("id")
                if not span_id:
                    continue
                span_text = current_span.text.strip()
                if not span_text:
                    try:
                        WebDriverWait(self.driver, 3).until(
                            lambda d, sid=span_id: d.find_element(By.ID, sid).text.strip() != ""
                        )
                        span_text = current_span.text.strip()
                    except TimeoutException:
                        span_text = ""
                contact_data[span_id] = span_text
            return contact_data
        return smart_wait_retry(_collect)
