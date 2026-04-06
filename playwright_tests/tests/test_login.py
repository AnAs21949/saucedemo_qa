from playwright.sync_api import expect
import pytest
import allure
from playwright_tests.pages.login_page import LoginPage
import re
import json


with open("data/project_data.json") as f:
    test_data = json.load(f)
    data = test_data["valid_credentials"]

@pytest.mark.smoke
@allure.epic("Authentication")
@allure.story("Valid Login")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("Verify successful login with valid credentials")
@pytest.mark.parametrize("data", data)
def test_valid_login(page, data):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(data["user_name"], data["password"])
    expect(page).to_have_url(re.compile(r"/inventory.html"))

@pytest.mark.regression
@pytest.mark.negative
@allure.epic("Authentication")
@allure.story("Login Failure")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Verify login fails with invalid credentials")
@pytest.mark.parametrize("data", test_data["invalid_credentials"])
def test_invalid_login(page, data):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(data["user_name"], data["password"])
    expect(login_page.error_locator()).to_be_visible()
    expect(login_page.error_locator()).to_contain_text("Epic sadface: Username and password do not match any user in this service" )


@pytest.mark.regression
@pytest.mark.negative
@allure.epic("Authentication")
@allure.story("Login Failure")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Verify locked out user cannot log in")
def test_locked_out_user(page):
    locked_data = test_data["locked_out_user"]
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(locked_data["user_name"], locked_data["password"])
    expect(login_page.error_locator()).to_contain_text(locked_data["expected_error"])



@pytest.mark.regression
@pytest.mark.negative
@allure.epic("Authentication")
@allure.story("Login Failure")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("Verify login fails with empty fields")
@pytest.mark.parametrize("data", test_data["empty_login_cases"])
def test_empty_fields_login(page, data):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login(data["user_name"], data["password"])
    expect(login_page.error_locator()).to_be_visible()
    expect(login_page.error_locator()).to_contain_text(data["expected_error"])