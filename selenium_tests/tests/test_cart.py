import allure
from pages.cart_page import CartPage
from pages.inventory_page import InventoryPage
import json
import pytest

with open("data/project_data.json") as f:
    data = json.load(f)


@pytest.mark.smoke
@allure.epic("Cart Management")
@allure.story("Add to Cart")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Verify item appears in cart after adding from product list")
def test_add_item_by_name(logged_in_driver):
    inventory_page = InventoryPage(logged_in_driver)
    inventory_page.add_to_cart(data["products"][0]["name"])
    inventory_page.go_to_cart()

    cart_page = CartPage(logged_in_driver)
    assert cart_page.get_item_names()[0] == data["products"][0]["name"]


@pytest.mark.regression
@allure.epic("Cart Management")
@allure.story("Remove from Cart")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Verify item is removed from cart page")
def test_remove_item(logged_in_driver):
    inventory_page = InventoryPage(logged_in_driver)
    inventory_page.add_to_cart(data["products"][0]["name"])
    inventory_page.go_to_cart()

    cart_page = CartPage(logged_in_driver)
    cart_page.remove_item(data["products"][0]["name"])
    assert len(cart_page.get_item_names()) == 0, "the remove operation has failed"


@pytest.mark.regression
@allure.epic("Cart Management")
@allure.story("View Cart")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Verify Continue Shopping returns to products page")
def test_return_to_shopping(logged_in_driver):
    inventory_page = InventoryPage(logged_in_driver)
    inventory_page.add_to_cart(data["products"][0]["name"])
    inventory_page.go_to_cart()

    cart_page = CartPage(logged_in_driver)
    cart_page.continue_shopping()
    inventory_page = InventoryPage(logged_in_driver)
    assert inventory_page.is_page_loaded(), "unable to go back to inventory page"


@pytest.mark.regression
@allure.epic("Cart Management")
@allure.story("View Cart")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Verify cart item quantity is correct")
def test_item_quantity(logged_in_driver):
    inventory_page = InventoryPage(logged_in_driver)
    inventory_page.add_to_cart(data["products"][0]["name"])
    inventory_page.go_to_cart()

    cart_page = CartPage(logged_in_driver)
    assert cart_page.get_item_quantities()[0] == 1


@pytest.mark.regression
@allure.epic("Cart Management")
@allure.story("View Cart")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Verify cart item price matches product price")
def test_item_price(logged_in_driver):
    inv = InventoryPage(logged_in_driver)
    inv.add_to_cart(data["products"][0]["name"])
    inv.go_to_cart()
    cart = CartPage(logged_in_driver)
    assert cart.get_item_prices()[0] == data["products"][0]["price"]
