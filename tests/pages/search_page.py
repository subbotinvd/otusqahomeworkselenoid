import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class SearchPage(BasePage):
    HEADING = (By.CSS_SELECTOR, "h1.page-title-section")
    PRODUCTS = (By.ID, "js-product-list")
    PRODUCTS_COUNT = (By.CSS_SELECTOR, "#js-product-list-top .products__count")
    PRODUCT_TILE = (By.CSS_SELECTOR, "#js-product-list article.product-miniature")
    NO_RESULTS = (By.CSS_SELECTOR, "#content.page-content--not-found")

    @allure.step("Check search results heading")
    def is_results_heading(self, query):
        self.logger.info("Checking search results heading for: %s", query)
        heading = self.get_text(*self.HEADING)
        assert "Search results" in heading, f"Unexpected heading: {heading}"
        assert query in heading, f"Query '{query}' not in heading: {heading}"
        return True

    @allure.step("Get number of found products")
    def get_products_count(self):
        self.logger.info("Counting found products")
        return len(self.find_all(*self.PRODUCT_TILE))

    @allure.step("Check products count block is visible")
    def check_products_count_visible(self):
        self.logger.info("Checking products count block")
        self.is_visible(*self.PRODUCTS_COUNT)

    @allure.step("Check that nothing was found")
    def is_no_results(self):
        self.logger.info("Checking no results block")
        return self.is_visible(*self.NO_RESULTS)
