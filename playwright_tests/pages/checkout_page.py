from .base_page import BasePage


class CheckoutPage(BasePage):
    def fill_personal_info(self, first_name, last_name, postal_code):
        self.page.fill("#first-name", first_name)
        self.page.fill("#last-name", last_name)
        self.page.fill("#postal-code", postal_code)

    def click_continue(self):
        self.page.locator("#continue").click()

    def click_cancel(self):
        self.page.locator("#cancel").click()

    def get_error_message(self):
        return self.page.locator("h3[data-test='error']").inner_text()

    def has_error(self):
        return self.page.locator("h3[data-test='error']").is_visible()