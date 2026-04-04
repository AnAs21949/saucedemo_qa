from .base_page import BasePage


class CartPage(BasePage):
    def get_item_names(self):
        return self.page.locator(".cart_item .inventory_item_name").all_inner_texts()

    def remove_item(self, product_name):
        item = product_name.replace(" ", "-").lower()
        self.page.locator(f"#remove-{item}").click()

    def go_to_checkout(self):
        self.page.locator("#checkout").click()

    def continue_shopping(self):
        self.page.locator("#continue-shopping").click()

    def get_item_count(self):
        return self.page.locator(".cart_item").count()

    def get_item_prices(self):
        texts = self.page.locator(".cart_item .inventory_item_price").all_inner_texts()
        return [float(p.replace("$", "")) for p in texts]

    def get_item_quantities(self):
        texts = self.page.locator(".cart_item .cart_quantity").all_inner_texts()
        return [int(q) for q in texts]

    def is_cart_page(self):
        return "cart.html" in self.page.url