
from selenium.webdriver.common.by import By
from pages.base_page import BasePage

class CartPage(BasePage):
    
    item_name = (By.CLASS_NAME, "inventory_item_name")
    checkout_button = (By.ID, "checkout")
    cart_items = (By.CLASS_NAME, "cart_item")
    continue_shopping_button = (By.ID, "continue-shopping")



    def get_item_names(self) -> list:
        try:
            return [
                item.find_element(By.CLASS_NAME, "inventory_item_name").text
                for item in self.find_elements(self.cart_items)
            ]
        except:
            return []
    
    def remove_item(self, product_name: str):
        item = product_name.replace(" ", "-").lower()
        self.click((By.ID, f"remove-{item}"))
        
    def go_to_checkout(self):
        self.click(self.checkout_button)
    
    def continue_shopping(self):
        self.click(self.continue_shopping_button)

    def get_item_count(self) -> int:
        return len(self.find_elements(self.cart_items))

    def get_item_prices(self) -> list:
        return [
            float(item.find_element(By.CLASS_NAME, "inventory_item_price").text.replace("$", ""))
            for item in self.find_elements(self.cart_items)
        ]

    def get_item_quantities(self) -> list:
        return [
            int(item.find_element(By.CLASS_NAME, "cart_quantity").text)
            for item in self.find_elements(self.cart_items)
        ]
    def is_cart_page(self):
        return "cart.html" in self.get_current_url()