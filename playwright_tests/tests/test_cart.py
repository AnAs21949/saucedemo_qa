from playwright.sync_api import expect
from playwright_tests.pages.cart_page import CartPage
from playwright_tests.pages.inventory_page import InventoryPage
import json
import pytest
import allure
import re


with open("data/project_data.json") as f:
    data = json.load(f)


@pytest.mark.smoke
@allure.epic("Cart Management")
@allure.story("Add to Cart")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Verify item appears in cart after adding from product list")
def test_add_item_by_name(logged_in_page):
    inv = InventoryPage(logged_in_page)
    inv.add_product_to_cart(data["products"][0]["name"])
    inv.go_to_cart()
    cart = CartPage(logged_in_page)
    assert cart.get_item_names()[0] == data["products"][0]["name"]


@pytest.mark.regression
@allure.epic("Cart Management")
@allure.story("Remove from Cart")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Verify item is removed from cart page")
def test_remove_item(logged_in_page):
    inv = InventoryPage(logged_in_page)
    inv.add_product_to_cart(data["products"][0]["name"])
    inv.go_to_cart()
    cart = CartPage(logged_in_page)
    cart.remove_item(data["products"][0]["name"])
    assert len(cart.get_item_names()) == 0


@pytest.mark.regression
@allure.epic("Cart Management")
@allure.story("View Cart")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Verify Continue Shopping returns to products page")
def test_return_to_shopping(logged_in_page):
    inv = InventoryPage(logged_in_page)
    inv.add_product_to_cart(data["products"][0]["name"])
    inv.go_to_cart()
    cart = CartPage(logged_in_page)
    cart.continue_shopping()
    expect(logged_in_page).to_have_url(re.compile("inventory"))


@pytest.mark.regression
@allure.epic("Cart Management")
@allure.story("View Cart")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Verify cart item quantity is correct")
def test_item_quantity(logged_in_page):
    inv = InventoryPage(logged_in_page)
    inv.add_product_to_cart(data["products"][0]["name"])
    inv.go_to_cart()
    cart = CartPage(logged_in_page)
    assert cart.get_item_quantities()[0] == 1


@pytest.mark.regression
@allure.epic("Cart Management")
@allure.story("View Cart")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Verify cart item price matches product price")
def test_item_price(logged_in_page):
    inv = InventoryPage(logged_in_page)
    inv.add_product_to_cart(data["products"][0]["name"])
    inv.go_to_cart()
    cart = CartPage(logged_in_page)
    assert cart.get_item_prices()[0] == data["products"][0]["price"]