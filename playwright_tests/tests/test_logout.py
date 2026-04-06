from playwright.sync_api import expect
from playwright_tests.pages.inventory_page import InventoryPage
from playwright_tests.pages.login_page import LoginPage
import pytest
import allure
import re


@pytest.mark.smoke
@allure.epic("Authentication")
@allure.story("Logout")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Verify logout redirects to login page")
def test_logout_redirects_to_login(logged_in_page):
    inv = InventoryPage(logged_in_page)
    inv.logout()
    expect(logged_in_page).to_have_url(re.compile("saucedemo.com/$|saucedemo.com$"))


@pytest.mark.regression
@allure.epic("Authentication")
@allure.story("Logout")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Verify session is invalidated after logout")
def test_session_invalid_after_logout(logged_in_page):
    inv = InventoryPage(logged_in_page)
    inv.logout()
    logged_in_page.go_back()
    login = LoginPage(logged_in_page)
    expect(login.error_locator()).to_contain_text("You can only access")