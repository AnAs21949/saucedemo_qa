
from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class ProductDetailPage(BasePage):

    product_name = (By.CLASS_NAME, "inventory_details_name")
    price_tag = (By.CLASS_NAME, "inventory_details_price")
    add_to_cart_button = (By.ID, "add-to-cart")
    remove_button = (By.ID, "remove")
    go_back_button = (By.ID, "back-to-products")

    def is_on_product_page(self) -> bool:
        return "inventory-item.html" in self.get_current_url()

    def get_product_name(self):
        return self.get_text(self.product_name)

    def get_price(self) -> float:
        return float(self.get_text(self.price_tag).replace("$", ""))
    
    def add_product_to_cart(self):
        self.click(self.add_to_cart_button)

    def remove_product_from_cart(self):
        self.click(self.remove_button)

    def go_back_to_inventory(self):
        self.click(self.go_back_button)