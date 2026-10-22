import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class ProductPage(BasePage):
    TITLE = (By.CSS_SELECTOR, "h1.product__name")
    PRICE = (By.CSS_SELECTOR, ".product__price")
    QUANTITY = (By.ID, "quantity_wanted")
    ADD_TO_CART = (By.CSS_SELECTOR, 'button[data-button-action="add-to-cart"]')
    BREADCRUMB = (By.CSS_SELECTOR, ".breadcrumb")
    ACCORDION_HEADER = (By.CSS_SELECTOR, "h2.accordion-header")
    CART_MODAL = (By.ID, "blockcart-modal")

    @allure.step("Open product page")
    def open(self, base_url):
        self.logger.info("Opening product page")
        super().open(f"{base_url}/index.php?controller=product&id_product=1")

    @allure.step("Check product page elements")
    def check_elements(self):
        self.logger.info("Checking product page elements")
        assert self.get_title().strip() != "", "Product title is empty"
        self.is_visible(*self.PRICE)
        self.is_visible(*self.QUANTITY)
        self.is_visible(*self.ADD_TO_CART)
        self.is_visible(*self.BREADCRUMB)
        assert len(self.find_all(*self.ACCORDION_HEADER)) > 0, "No description sections"

    @allure.step("Get product title")
    def get_title(self):
        self.logger.info("Getting product title")
        return self.get_text(*self.TITLE)

    @allure.step("Add product to cart")
    def add_to_cart(self):
        self.logger.info("Adding product to cart")
        self.click(*self.ADD_TO_CART)
        self.is_visible(*self.CART_MODAL)

    @allure.step("Check product '{name}' is in cart modal")
    def is_product_in_cart_modal(self, name):
        self.logger.info("Checking cart modal contains product: %s", name)
        return self.wait.until(
            EC.text_to_be_present_in_element(self.CART_MODAL, name)
        )
