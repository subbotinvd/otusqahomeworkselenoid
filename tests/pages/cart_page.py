import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CartPage(BasePage):
    HEADING = (By.CSS_SELECTOR, "h1")
    CART_ITEM = (By.CSS_SELECTOR, ".cart__item")
    REMOVE_LINK = (By.CSS_SELECTOR, ".js-remove-from-cart")
    TOTALS = (By.CSS_SELECTOR, ".cart-summary__totals")

    @allure.step("Open cart page")
    def open(self, base_url):
        self.logger.info("Opening cart page")
        super().open(f"{base_url}/index.php?controller=cart")

    @allure.step("Check cart page elements")
    def check_elements(self):
        self.logger.info("Checking cart page elements")
        heading = self.get_text(*self.HEADING)
        assert heading.strip() == "Shopping Cart", f"Unexpected cart heading: {heading}"
        self.is_visible(*self.TOTALS)

    @allure.step("Get number of items in cart")
    def get_items_count(self):
        self.logger.info("Counting items in cart")
        return len(self.find_all(*self.CART_ITEM))
