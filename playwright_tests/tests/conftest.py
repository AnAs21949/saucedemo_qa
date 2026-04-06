import pytest
from playwright.sync_api import sync_playwright
from playwright_tests.pages.login_page import LoginPage


def pytest_addoption(parser):
    parser.addoption("--headless", action="store_true", default=False)


@pytest.fixture(scope="session")
def browser(request):
    headless = request.config.getoption("--headless")
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=headless)
    yield browser
    browser.close()
    pw.stop()


@pytest.fixture(scope="function")
def context(browser):
    context = browser.new_context()
    yield context
    context.close()


@pytest.fixture(scope="function")
def page(context):
    page = context.new_page()
    yield page
    page.close()


@pytest.fixture(scope="function")
def logged_in_page(page):
    login_page = LoginPage(page)
    login_page.open()
    login_page.login("standard_user", "secret_sauce")
    return page