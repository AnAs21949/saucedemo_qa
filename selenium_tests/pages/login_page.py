from selenium.webdriver.common.by import By
from .base_page import BasePage
from utils.config_loader import config


class LoginPage(BasePage):
    username_input = (By.ID, "user-name")
    password_input = (By.ID, "password")
    login_button = (By.ID, "login-button")
    error_message = (By.XPATH, "//h3[@data-test = 'error']")

    def open(self):
        super().open(config["base_url"])

    def enter_login_credentials(self, username, password):
        self.clear_and_type(self.username_input, username)
        self.clear_and_type(self.password_input, password)
        self.click(self.login_button)

    def get_error_message(self):
        return self.get_text(self.error_message)
