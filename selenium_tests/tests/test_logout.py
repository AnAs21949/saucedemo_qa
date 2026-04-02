import allure
import pytest
from pages.inventory_page import InventoryPage
from pages.login_page import LoginPage


@pytest.mark.smoke
@allure.epic("Authentication")
@allure.story("Logout")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Verify logout redirects to login page")
def test_logout_redirects_to_login(logged_in_driver):
    inv = InventoryPage(logged_in_driver)
    inv.logout()
    login = LoginPage(logged_in_driver)
    assert login.is_element_visible(login.login_button), "Login page not displayed after logout"


@pytest.mark.regression
@allure.epic("Authentication")
@allure.story("Logout")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Verify session is invalidated after logout")
def test_session_invalid_after_logout(logged_in_driver):
    inv = InventoryPage(logged_in_driver)
    inv.logout()
    logged_in_driver.back()
    login = LoginPage(logged_in_driver)
    assert "Epic sadface: You can only access '/inventory.html' when you are logged in." in login.get_error_message()
