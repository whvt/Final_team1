from Tests.UI.pages.base_page import BasePage
from Tests.config.user_creds import USER_CREDS


class LoginPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)
        self.url = "https://thinking-tester-contact-list.herokuapp.com/"
        self.username_input = ("id", "email")
        self.password_input = ("id", "password")
        self.login_button = ("id", "submit")

    def open(self):
        self.driver.get(self.url)

    def login(self):
        self.wait_for_element(self.username_input).send_keys(USER_CREDS["username"])
        self.wait_for_element(self.password_input).send_keys(USER_CREDS["password"])
        self.wait_for_element(self.login_button).click()
