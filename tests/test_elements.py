import allure

from pages.main_page import MainPage
from pages.catalog_page import CatalogPage
from pages.product_page import ProductPage
from pages.admin_login_page import AdminLoginPage
from pages.registration_page import RegistrationPage


@allure.feature("UI Elements")
class TestPageElements:

    @allure.story("Main Page")
    @allure.title("Check main page elements")
    def test_main_page_elements(self, driver, base_url):
        page = MainPage(driver)
        page.open(base_url)
        page.check_elements()

    @allure.story("Catalog Page")
    @allure.title("Check catalog page elements")
    def test_catalog_page_elements(self, driver, base_url):
        page = CatalogPage(driver)
        page.open(base_url)
        page.check_elements()

    @allure.story("Product Page")
    @allure.title("Check product page elements")
    def test_product_page_elements(self, driver, base_url):
        page = ProductPage(driver)
        page.open(base_url)
        page.check_elements()

    @allure.story("Admin Login Page")
    @allure.title("Check admin login page elements")
    def test_admin_login_page_elements(self, driver, base_url, admin_folder):
        page = AdminLoginPage(driver)
        page.open(base_url, admin_folder)
        page.check_elements()

    @allure.story("Registration Page")
    @allure.title("Check registration page elements")
    def test_registration_page_elements(self, driver, base_url):
        page = RegistrationPage(driver)
        page.open(base_url)
        page.check_elements()
