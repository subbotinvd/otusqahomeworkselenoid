import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CatalogPage(BasePage):
    HEADING = (By.CSS_SELECTOR, "h1.page-title-section")
    PRODUCTS = (By.ID, "js-product-list")
    FILTERS = (By.ID, "search-filters")
    SORT = (By.CSS_SELECTOR, ".products__sort")
    PAGINATION = (By.CSS_SELECTOR, ".products__pagination")
    PRODUCT_TILE = (By.CSS_SELECTOR, "#js-product-list article.product-miniature")

    @allure.step("Open catalog page")
    def open(self, base_url):
        self.logger.info("Opening catalog page")
        super().open(f"{base_url}/index.php?controller=category&id_category=3")

    @allure.step("Check catalog page elements")
    def check_elements(self):
        self.logger.info("Checking catalog page elements")
        heading = self.get_text(*self.HEADING)
        assert heading.strip() == "Clothes", f"Unexpected catalog heading: {heading}"
        self.is_visible(*self.PRODUCTS)
        self.is_visible(*self.FILTERS)
        self.is_visible(*self.SORT)
        self.is_visible(*self.PAGINATION)
        assert self.get_products_count() > 0, "No products in catalog"

    @allure.step("Get number of products on page")
    def get_products_count(self):
        self.logger.info("Counting products on page")
        return len(self.find_all(*self.PRODUCT_TILE))
