from .base_page import BasePage


class ProductDetailPage(BasePage):
    def is_on_product_page(self):
        return "inventory-item.html" in self.page.url

    def get_product_name(self):
        return self.page.locator(".inventory_details_name").inner_text()

    def get_price(self):
        text = self.page.locator(".inventory_details_price").inner_text()
        return float(text.replace("$", ""))

    def add_product_to_cart(self):
        self.page.locator("#add-to-cart").click()

    def remove_product_from_cart(self):
        self.page.locator("#remove").click()

    def go_back_to_inventory(self):
        self.page.locator("#back-to-products").click()