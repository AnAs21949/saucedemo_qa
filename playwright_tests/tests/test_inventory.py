from playwright.sync_api import expect
from playwright_tests.pages.inventory_page import InventoryPage
import pytest
import allure
import json

with open("data/project_data.json") as f:
    data = json.load(f)


@pytest.mark.smoke
@allure.epic("Product Catalog")
@allure.story("Product List")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Verify 6 products are displayed")
def test_six_products_load(logged_in_page):
    inv = InventoryPage(logged_in_page)
    names = inv.get_product_names()
    assert len(names) == 6


@pytest.mark.regression
@allure.epic("Product Catalog")
@allure.story("Sort Products")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Verify sort by Name A to Z")
def test_sort_a_to_z(logged_in_page):
    inv = InventoryPage(logged_in_page)
    inv.sort_products("az")
    names = inv.get_product_names()
    assert names == sorted(names)


@pytest.mark.regression
@allure.epic("Product Catalog")
@allure.story("Sort Products")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Verify sort by Name Z to A")
def test_sort_z_to_a(logged_in_page):
    inv = InventoryPage(logged_in_page)
    inv.sort_products("za")
    names = inv.get_product_names()
    assert names == sorted(names, reverse=True)


@pytest.mark.regression
@allure.epic("Product Catalog")
@allure.story("Sort Products")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Verify sort by Price low to high")
def test_sort_price_low_to_high(logged_in_page):
    inv = InventoryPage(logged_in_page)
    inv.sort_products("lohi")
    prices = inv.get_product_prices()
    float_prices = [float(p.replace("$", "")) for p in prices]
    assert float_prices == sorted(float_prices)


@pytest.mark.regression
@allure.epic("Product Catalog")
@allure.story("Sort Products")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Verify sort by Price high to low")
def test_sort_price_high_to_low(logged_in_page):
    inv = InventoryPage(logged_in_page)
    inv.sort_products("hilo")
    prices = inv.get_product_prices()
    float_prices = [float(p.replace("$", "")) for p in prices]
    assert float_prices == sorted(float_prices, reverse=True)


@pytest.mark.smoke
@allure.epic("Cart Management")
@allure.story("Cart Badge")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Verify cart badge increments when adding items")
def test_cart_badge_increments(logged_in_page):
    inv = InventoryPage(logged_in_page)
    assert inv.get_cart_count() == 0
    inv.add_product_to_cart(data["products"][0]["name"])
    assert inv.get_cart_count() == 1
    inv.add_product_to_cart(data["products"][1]["name"])
    assert inv.get_cart_count() == 2


@pytest.mark.regression
@allure.epic("Cart Management")
@allure.story("Cart Badge")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Verify cart badge decrements when removing items")
def test_cart_badge_decrements(logged_in_page):
    inv = InventoryPage(logged_in_page)
    inv.add_product_to_cart(data["products"][0]["name"])
    assert inv.get_cart_count() == 1
    inv.remove_product_from_cart(data["products"][0]["name"])
    assert inv.get_cart_count() == 0


@pytest.mark.regression
@allure.epic("Product Catalog")
@allure.story("Product List")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Verify product card shows name, price, and description")
def test_product_card_shows_complete_info(logged_in_page):
    inv = InventoryPage(logged_in_page)
    names = inv.get_product_names()
    prices = inv.get_product_prices()
    assert len(names) == 6
    assert len(prices) == 6
    assert all(name != "" for name in names)
    assert all(p != "" for p in prices)


@pytest.mark.regression
@allure.epic("Product Catalog")
@allure.story("Sort Products")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Verify sort dropdown has four options")
def test_sort_dropdown_has_four_options(logged_in_page):
    inv = InventoryPage(logged_in_page)
    options = inv.get_sort_options()
    assert len(options) == 4
    assert "Name (A to Z)" in options
    assert "Name (Z to A)" in options
    assert "Price (low to high)" in options
    assert "Price (high to low)" in options


@pytest.mark.regression
@allure.epic("Cart Management")
@allure.story("Cart Badge")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Verify cart badge disappears when cart is empty")
def test_cart_badge_disappears_when_empty(logged_in_page):
    inv = InventoryPage(logged_in_page)
    inv.add_product_to_cart(data["products"][0]["name"])
    assert inv.get_cart_count() == 1
    inv.remove_product_from_cart(data["products"][0]["name"])
    assert inv.get_cart_count() == 0


@pytest.mark.regression
@allure.epic("Cart Management")
@allure.story("Remove from Cart")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Verify remove reverts button to Add to cart")
def test_remove_reverts_to_add_button(logged_in_page):
    inv = InventoryPage(logged_in_page)
    product = data["products"][0]["name"]
    inv.add_product_to_cart(product)
    inv.remove_product_from_cart(product)
    assert inv.is_add_to_cart_visible(product)