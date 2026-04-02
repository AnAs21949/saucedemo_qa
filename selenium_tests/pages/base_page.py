from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from utils.config_loader import config
import logging


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, config["timeout"])
        self.logger = logging.getLogger(self.__class__.__name__)
    
    def open(self, url):
        self.logger.info(f"Opening URL: {url}")
        self.driver.get(url)
    
    def click(self, locator):
        self.logger.debug(f"Clicking on element: {locator}")
        self.wait.until(EC.element_to_be_clickable(locator)).click()
    
    def clear_and_type(self, locator, text):
        self.logger.debug(f"Typing text into element: {locator}")
        element = self.wait.until(EC.visibility_of_element_located(locator))
        element.clear()
        element.send_keys(text)

    def get_text(self, locator):
        self.logger.debug(f"Getting text from element: {locator}")
        return self.wait.until(EC.visibility_of_element_located(locator)).text
    
    def find_elements(self, locator):
        return self.wait.until(EC.presence_of_all_elements_located(locator))
    
    def is_element_visible(self, locator) -> bool:
        try:
            return self.wait.until(EC.visibility_of_element_located(locator)).is_displayed()
        except Exception:
            return False
        
    def get_current_url(self) -> str:
        return self.driver.current_url