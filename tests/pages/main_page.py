import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from pages.base_page import BasePage


class MainPage(BasePage):
    HEADER = (By.ID, "header")
    SEARCH_INPUT = (By.ID, "ps_searchbar_input")
    CART = (By.CSS_SELECTOR, ".cart-preview")
    MENU = (By.CSS_SELECTOR, ".ps-mainmenu")
    CONTACT = (By.ID, "_desktop_ps_contactinfo")
    PRODUCT_TILE = (By.CSS_SELECTOR, "article.product-miniature")
    PRODUCT_PRICE = (By.CSS_SELECTOR, "article.product-miniature .product-miniature__price")
    FIRST_PRODUCT_LINK = (
        By.CSS_SELECTOR,
        "article.product-miniature .product-miniature__image-link",
    )

    @allure.step("Open main page")
    def open(self, base_url):
        self.logger.info("Opening main page: %s", base_url)
        super().open(base_url)

    @allure.step("Check main page elements")
    def check_elements(self):
        self.logger.info("Checking main page elements")
        self.is_visible(*self.HEADER)
        self.is_visible(*self.SEARCH_INPUT)
        self.is_visible(*self.CART)
        self.is_visible(*self.MENU)
        self.is_visible(*self.CONTACT)
        assert self.get_products_count() > 0, "No products on main page"

    @allure.step("Get number of products on page")
    def get_products_count(self):
        self.logger.info("Counting products on page")
        return len(self.find_all(*self.PRODUCT_TILE))

    @allure.step("Search for '{query}'")
    def search(self, query):
        self.logger.info("Searching for: %s", query)
        self.input_text(*self.SEARCH_INPUT, query)
        self.find(*self.SEARCH_INPUT).send_keys(Keys.ENTER)

    @allure.step("Open first product page")
    def open_first_product(self):
        self.logger.info("Opening first product page")
        self.click(*self.FIRST_PRODUCT_LINK)
