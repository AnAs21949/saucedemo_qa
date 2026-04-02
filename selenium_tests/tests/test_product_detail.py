import allure
import pytest
from pages.product_detail_page import ProductDetailPage
from pages.inventory_page import InventoryPage
import json

with open("data/project_data.json") as f:
    data = json.load(f)


@pytest.mark.smoke
@allure.epic("Product Catalog")
@allure.story("Product Detail")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Verify product detail page is accessible")
def test_product_availability(logged_in_driver):
    inventory_page = InventoryPage(logged_in_driver)
    inventory_page.click_product(data["products"][0]["name"])
    detail = ProductDetailPage(logged_in_driver)
    assert detail.is_on_product_page()


@pytest.mark.regression
@allure.epic("Product Catalog")
@allure.story("Product Detail")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Verify product name and price match listing")
@pytest.mark.parametrize("product", data["products"])
def test_product_match(logged_in_driver, product):
    inv = InventoryPage(logged_in_driver)
    inv.click_product(product["name"])
    detail = ProductDetailPage(logged_in_driver)
    assert detail.get_product_name() == product["name"]
    assert detail.get_price() == product["price"]


@pytest.mark.regression
@allure.epic("Cart Management")
@allure.story("Add to Cart")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Verify add to cart from product detail page")
def test_add_to_cart_from_product_page(logged_in_driver):
    inventory_page = InventoryPage(logged_in_driver)
    inventory_page.click_product(data["products"][0]["name"])
    product_detail_page = ProductDetailPage(logged_in_driver)
    product_detail_page.add_product_to_cart()
    assert inventory_page.get_cart_count() == 1


@pytest.mark.regression
@allure.epic("Product Catalog")
@allure.story("Product Detail")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Verify Back to Products returns to inventory")
def test_go_back_to_inventory(logged_in_driver):
    inventory_page = InventoryPage(logged_in_driver)
    inventory_page.click_product(data["products"][0]["name"])
    product_detail_page = ProductDetailPage(logged_in_driver)
    product_detail_page.go_back_to_inventory()
    assert inventory_page.is_page_loaded()
