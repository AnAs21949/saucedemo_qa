from .base_page import BasePage


class InventoryPage(BasePage):
    def __init__(self, page):
        super().__init__(page)
        self.url = "https://www.saucedemo.com/inventory.html"

    def get_product_names(self):
        return self.page.locator(".inventory_item_name").all_inner_texts()

    def get_product_prices(self):
        return self.page.locator(".inventory_item_price").all_inner_texts()

    def add_product_to_cart(self, product_name):
        product_locator = self.page.locator(f".inventory_item:has-text('{product_name}')")
        product_locator.locator("button").click()

    def remove_product_from_cart(self, product_name):
        product_locator = self.page.locator(f".inventory_item:has-text('{product_name}')")
        product_locator.locator("button").click()

    def get_cart_count(self):
        cart_badge = self.page.locator(".shopping_cart_badge")
        if cart_badge.is_visible():
            return int(cart_badge.inner_text())
        return 0

    def go_to_cart(self):
        self.page.locator(".shopping_cart_link").click()

    def sort_products(self, sort_option):
        self.page.select_option(".product_sort_container", sort_option)

    def get_sort_options(self):
        return self.page.locator(".product_sort_container option").all_inner_texts()

    def logout(self):
        self.page.locator("#react-burger-menu-btn").click()
        self.page.locator("#logout_sidebar_link").click()

    def click_product(self, product_name):
        self.page.get_by_text(product_name, exact=True).click()

    def is_add_to_cart_visible(self, product_name):
        item = product_name.replace(" ", "-").lower()
        return self.page.locator(f"#add-to-cart-{item}").is_visible()