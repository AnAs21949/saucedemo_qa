import pytest
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def browser():
    pw = sync_playwright().start()
    browser = pw.chromium.launch(headless=False)
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