from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class CheckoutOverviewPage(BasePage):

    product_name = (By.CLASS_NAME, "inventory_item_name")
    summary_subtotal = (By.CLASS_NAME, "summary_subtotal_label")
    total_price = (By.CLASS_NAME, "summary_total_label")
    tax_price = (By.CLASS_NAME, "summary_tax_label")
    finish_button = (By.ID, "finish")
    cancel_button = (By.ID, "cancel")
    success_message = (By.CLASS_NAME, "complete-header")
    back_home_button = (By.ID, "back-to-products")


    def get_product_names(self):
        return [item.text for item in self.find_elements(self.product_name)]
    
    def has_product(self, name: str) -> bool:
        return name in self.get_product_names()
    
    def get_price(self) -> float:
        return float(self.get_text(self.summary_subtotal).split("$")[-1])
    
    def get_total_price(self) -> float:
        return float(self.get_text(self.total_price).split("$")[-1])
    
    def get_tax_price(self) -> float:
        return float(self.get_text(self.tax_price).split("$")[-1])
    
    def click_finish_button(self):
        self.click(self.finish_button)

    def click_cancel_button(self):
        self.click(self.cancel_button)

    def total_matches_items_plus_tax(self) -> bool:
        expected = round(self.get_price() + self.get_tax_price(), 2)
        actual   = round(self.get_total_price(), 2)
        return expected == actual

    def get_success_message(self) -> str:
        return self.get_text(self.success_message)

    def is_on_success_page(self) -> bool:
        return "checkout-complete" in self.get_current_url()

    def click_back_home(self):
        self.click(self.back_home_button)