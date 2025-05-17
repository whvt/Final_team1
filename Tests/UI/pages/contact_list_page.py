"""Contact list page"""


from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from Tests.UI.pages.base_page import BasePage


class ContactListPage(BasePage):
    """Contact list page class"""
    def __init__(self, driver):
        super().__init__(driver)
        self.num = 1
        self.logout_button = ("id", "logout")
        self.add_contact_button = ("id", "add-contact")
        self.contact_table_rows = ("css selector", "tr.contactTableBodyRow")
        self.contact_data_button = (By.XPATH, f"//tr[@class='contactTableBodyRow'][{self.num}]")

    def click_contact_data(self):
        """click contact data button"""
        self.wait_for_element(self.contact_data_button).click()

    def logout(self):
        """click logout button"""
        self.wait_for_element(self.logout_button).click()

    def click_add_contact(self):
        """click add contact button"""
        self.wait_for_element(self.add_contact_button).click()

    def get_contacts(self):
        """get contacts in list table"""
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "tr.contactTableBodyRow")
            )
        )
        rows = self.driver.find_elements(By.CSS_SELECTOR, "tr.contactTableBodyRow")
        contacts = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            contacts.append(
                {
                    "id": cells[0].get_attribute("textContent").strip(),
                    "name": cells[1].text.strip(),
                    "birthdate": cells[2].text.strip(),
                    "email": cells[3].text.strip(),
                    "phone": cells[4].text.strip(),
                    "address": cells[5].text.strip(),
                    "location": cells[6].text.strip(),
                    "country": cells[7].text.strip(),
                }
            )
        return contacts

    @staticmethod
    def no_contacts(contacts_est1, contacts_est2):
        """check contact exist"""
        if contacts_est2 < contacts_est1:
            return True
        return False

    def contact_list_table_header(self):
        """contact list table header check"""
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "myTable"))
        )
        contact_table = self.driver.find_element(By.ID, "myTable")
        headers = contact_table.find_elements(By.TAG_NAME, "th")
        return headers

    def contact_list_table_structure(self):
        """contact list table structure check"""
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "myTable"))
        )
        contact_table = self.driver.find_element(By.ID, "myTable")
        rows = contact_table.find_elements(By.TAG_NAME, "tr")
        raw_len = True
        if len(rows) > 1:
            for row in rows[1:]:
                cells = row.find_elements(By.TAG_NAME, "td")
                if len(cells) < 7:
                    raw_len = False
                    return raw_len
        return raw_len

    def contact_list_table_duplicates(self):
        """contact list table duplicates check"""
        WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located(
                (By.CSS_SELECTOR, "tr.contactTableBodyRow")
            )
        )
        rows = self.driver.find_elements(By.CSS_SELECTOR, "tr.contactTableBodyRow")
        contacts = []
        for row in rows:
            cells = row.find_elements(By.TAG_NAME, "td")
            contact = (
                cells[0].text.strip(),  # name
                cells[1].text.strip(),  # birthdate
                cells[2].text.strip(),  # email
                cells[3].text.strip(),  # phone
                cells[4].text.strip(),  # address
                cells[5].text.strip(),  # city, state/Province, postal code
                cells[6].text.strip(),  # country
            )
            contacts.append(contact)
        duplicates = set()
        checked = set()
        for contact in contacts:
            if contact in checked:
                duplicates.add(contact)
            checked.add(contact)
        return duplicates
