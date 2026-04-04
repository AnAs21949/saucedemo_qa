from .base_page import BasePage


class CheckoutOverviewPage(BasePage):
    def get_product_names(self):
        return self.page.locator(".inventory_item_name").all_inner_texts()

    def has_product(self, name):
        return name in self.get_product_names()

    def get_price(self):
        text = self.page.locator(".summary_subtotal_label").inner_text()
        return float(text.split("$")[-1])

    def get_total_price(self):
        text = self.page.locator(".summary_total_label").inner_text()
        return float(text.split("$")[-1])

    def get_tax_price(self):
        text = self.page.locator(".summary_tax_label").inner_text()
        return float(text.split("$")[-1])

    def click_finish_button(self):
        self.page.locator("#finish").click()

    def click_cancel_button(self):
        self.page.locator("#cancel").click()

    def total_matches_items_plus_tax(self):
        expected = round(self.get_price() + self.get_tax_price(), 2)
        actual = round(self.get_total_price(), 2)
        return expected == actual

    def get_success_message(self):
        return self.page.locator(".complete-header").inner_text()

    def is_on_success_page(self):
        return "checkout-complete" in self.page.url

    def click_back_home(self):
        self.page.locator("#back-to-products").click()