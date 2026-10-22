import logging

import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 10)
        self.logger = logging.getLogger(self.__class__.__name__)

    @allure.step("Open URL {url}")
    def open(self, url):
        self.logger.info("Opening URL: %s", url)
        self.driver.get(url)

    @allure.step("Find element {by}={value}")
    def find(self, by, value):
        self.logger.info("Finding element: %s=%s", by, value)
        return self.driver.find_element(by, value)

    @allure.step("Find all elements {by}={value}")
    def find_all(self, by, value):
        self.logger.info("Finding all elements: %s=%s", by, value)
        return self.driver.find_elements(by, value)

    @allure.step("Click element {by}={value}")
    def click(self, by, value):
        self.logger.info("Clicking element: %s=%s", by, value)
        element = self.wait.until(EC.element_to_be_clickable((by, value)))
        self._scroll_into_view(element)
        element.click()

    @allure.step("Click first clickable of given locators")
    def click_any(self, *locators, timeout=2):
        self.logger.info("Clicking first clickable of %d locators", len(locators))
        for locator in locators:
            try:
                element = WebDriverWait(self.driver, timeout).until(
                    EC.element_to_be_clickable(locator)
                )
            except TimeoutException:
                continue
            self._scroll_into_view(element)
            element.click()
            return element
        raise TimeoutException(
            f"None of the {len(locators)} locators became clickable"
        )

    def _scroll_into_view(self, element):
        needs_scroll = not self.driver.execute_script(
            "const rect = arguments[0].getBoundingClientRect();"
            "return rect.top >= 0 && rect.bottom <= window.innerHeight"
            " && rect.left >= 0 && rect.right <= window.innerWidth;",
            element,
        )
        if needs_scroll:
            self.driver.execute_script(
                "arguments[0].scrollIntoView({block: 'center', behavior: 'instant'});",
                element,
            )

    @allure.step("Input text into {by}={value}")
    def input_text(self, by, value, text):
        self.logger.info("Inputting text into %s=%s", by, value)
        element = self.wait.until(EC.visibility_of_element_located((by, value)))
        element.clear()
        element.send_keys(text)

    @allure.step("Get text of {by}={value}")
    def get_text(self, by, value):
        self.logger.info("Getting text of element: %s=%s", by, value)
        return self.wait.until(EC.visibility_of_element_located((by, value))).text

    @allure.step("Check visibility of {by}={value}")
    def is_visible(self, by, value):
        self.logger.info("Checking visibility: %s=%s", by, value)
        return self.wait.until(EC.visibility_of_element_located((by, value)))

    @allure.step("Check presence of {by}={value}")
    def is_present(self, by, value):
        self.logger.info("Checking presence: %s=%s", by, value)
        return self.wait.until(EC.presence_of_element_located((by, value)))
