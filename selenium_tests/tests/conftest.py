from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
import pytest


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome")
    parser.addoption("--headless", action="store_true", default=False)

@pytest.fixture
def driver(request):
    browser = request.config.getoption("--browser")
    headless = request.config.getoption("--headless")

    if browser == "chrome":
        options = Options()
        options.add_argument("--incognito")
        options.add_argument("--disable-notifications")
        if headless:
            options.add_argument("--headless=new")
            options.add_argument("--disable-dev-shm-usage")
            options.add_argument("--no-sandbox")
        options.add_experimental_option("prefs", {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        })
        driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)
    elif browser == "firefox":
        driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()))
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    driver.maximize_window()
    yield driver
    driver.quit()


@pytest.fixture
def logged_in_driver(driver):
    from pages.login_page import LoginPage
    login = LoginPage(driver)
    login.open()
    login.enter_login_credentials("standard_user", "secret_sauce")
    return driver

@pytest.hookimpl( hookwrapper=True )
def pytest_runtest_makereport(item):
    """
        Extends the PyTest Plugin to take and embed screenshot in html report, whenever test fails.
        :param item:
        """
    pytest_html = item.config.pluginmanager.getplugin( 'html' )
    outcome = yield
    report = outcome.get_result()
    extra = getattr( report, 'extra', [] )

    if report.when == 'call' or report.when == "setup":
        xfail = hasattr( report, 'wasxfail' )
        if (report.skipped and xfail) or (report.failed and not xfail):
            driver = item.funcargs.get("driver") or item.funcargs.get("logged_in_driver")
            if driver and pytest_html:
                screenshot = driver.get_screenshot_as_base64()
                html = '<div><img src="data:image/png;base64,%s" style="width:304px;height:228px;" ' \
                       'onclick="window.open(this.src)" align="right"/></div>' % screenshot
                extra.append( pytest_html.extras.html( html ) )
        report.extras = extra
