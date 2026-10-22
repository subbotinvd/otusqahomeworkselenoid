import allure

from pages.main_page import MainPage
from pages.search_page import SearchPage


@allure.feature("Search")
class TestSearch:

    @allure.story("Search Results")
    @allure.title("Search finds matching products")
    def test_search_finds_products(self, driver, base_url):
        main = MainPage(driver)
        main.open(base_url)
        main.search("mug")

        results = SearchPage(driver)
        assert results.is_results_heading("mug")
        results.check_products_count_visible()
        assert results.get_products_count() > 0, "No products found by search"

    @allure.story("Search Results")
    @allure.title("Search without matches shows no results block")
    def test_search_no_results(self, driver, base_url):
        main = MainPage(driver)
        main.open(base_url)
        main.search("qwerty_no_such_product_12345")

        results = SearchPage(driver)
        assert results.is_no_results()
