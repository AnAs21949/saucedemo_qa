from playwright.sync_api import expect
from playwright_tests.pages.inventory_page import InventoryPage
from playwright_tests.pages.cart_page import CartPage
from playwright_tests.pages.checkout_page import CheckoutPage
from playwright_tests.pages.checkout_overview_page import CheckoutOverviewPage
import pytest
import allure
import json
import re

with open("data/project_data.json") as f:
    data = json.load(f)


def reach_checkout_step1(page):
    inv = InventoryPage(page)
    inv.add_product_to_cart(data["products"][0]["name"])
    inv.go_to_cart()
    CartPage(page).go_to_checkout()
    return CheckoutPage(page)


def reach_checkout_step2(page):
    checkout = reach_checkout_step1(page)
    checkout.fill_personal_info(
        data["valid_credentials"][0]["first_name"],
        data["valid_credentials"][0]["last_name"],
        data["valid_credentials"][0]["postal_code"]
    )
    checkout.click_continue()
    return CheckoutOverviewPage(page)


@pytest.mark.smoke
@allure.epic("Checkout")
@allure.story("Complete Purchase")
@allure.severity(allure.severity_level.BLOCKER)
@allure.title("Verify full checkout flow completes successfully")
def test_full_checkout(logged_in_page):
    overview = reach_checkout_step2(logged_in_page)
    overview.click_finish_button()
    assert overview.is_on_success_page()


@pytest.mark.negative
@pytest.mark.regression
@allure.epic("Checkout")
@allure.story("Shipping Information")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Verify error on empty checkout fields")
@pytest.mark.parametrize("case", data["checkout_empty_field_cases"])
def test_empty_field_error(logged_in_page, case):
    checkout = reach_checkout_step1(logged_in_page)
    checkout.fill_personal_info(case["first_name"], case["last_name"], case["postal_code"])
    checkout.click_continue()
    assert checkout.has_error()
    assert case["expected_error"] in checkout.get_error_message()


@pytest.mark.regression
@allure.epic("Checkout")
@allure.story("Shipping Information")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Verify cancel on step 1 returns to cart")
def test_cancel_step1_returns_to_cart(logged_in_page):
    checkout = reach_checkout_step1(logged_in_page)
    checkout.click_cancel()
    expect(logged_in_page).to_have_url(re.compile("cart"))


@pytest.mark.regression
@allure.epic("Checkout")
@allure.story("Order Review")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Verify order total matches items plus tax")
def test_price_math(logged_in_page):
    overview = reach_checkout_step2(logged_in_page)
    assert overview.total_matches_items_plus_tax()


@pytest.mark.regression
@allure.epic("Checkout")
@allure.story("Order Review")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Verify cancel on step 2 returns to inventory")
def test_cancel_step2_returns_to_inventory(logged_in_page):
    overview = reach_checkout_step2(logged_in_page)
    overview.click_cancel_button()
    expect(logged_in_page).to_have_url(re.compile("inventory"))


@pytest.mark.regression
@allure.epic("Checkout")
@allure.story("Complete Purchase")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Verify Back Home returns to products after purchase")
def test_back_home_after_purchase(logged_in_page):
    overview = reach_checkout_step2(logged_in_page)
    overview.click_finish_button()
    assert overview.is_on_success_page()
    overview.click_back_home()
    expect(logged_in_page).to_have_url(re.compile("inventory"))