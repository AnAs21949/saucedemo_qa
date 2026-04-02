from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutPage(BasePage):
    
    user_name_input =(By.ID, "first-name")
    last_name_input = (By.ID, "last-name") 
    postal_code_input = (By.ID, "postal-code")
    continue_button = (By.ID, "continue")
    cancel_button = (By.ID, "cancel")
    error_message = (By.XPATH, "//h3[@data-test='error']")
       
    def fill_personal_info(self, first_name, last_name, postal_code):
        self.clear_and_type(self.user_name_input, first_name)
        self.clear_and_type(self.last_name_input, last_name)
        self.clear_and_type(self.postal_code_input, postal_code)

    def click_continue(self):
        self.click(self.continue_button)

    def click_cancel(self):
        self.click(self.cancel_button)
    
    def get_error_message(self) -> str:
        return self.get_text(self.error_message)
    
    def has_error(self) -> bool:
        return self.is_element_visible(self.error_message)
    