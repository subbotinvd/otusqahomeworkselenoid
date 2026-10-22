import allure

from pages.admin_login_page import AdminLoginPage
from pages.admin_dashboard_page import AdminDashboardPage
from pages.admin_product_page import AdminProductPage


@allure.feature("Admin Products")
class TestAdminProduct:

    @allure.story("CRUD")
    @allure.title("Add new product")
    def test_add_new_product(self, driver, base_url, admin_email, admin_password, admin_folder):
        login = AdminLoginPage(driver)
        login.open(base_url, admin_folder)
        login.login(admin_email, admin_password)

        dashboard = AdminDashboardPage(driver)
        dashboard.check_logged_in()

        products = AdminProductPage(driver)
        products.open_products(base_url, admin_folder)
        products.check_products_list()
        products.open_create_page(base_url, admin_folder)
        products.choose_standard_type()
        products.fill_product_form(name="Test Product", price="99.99", qty="10")
        assert products.save()

    @allure.story("CRUD")
    @allure.title("Delete product")
    def test_delete_product(self, driver, base_url, admin_email, admin_password, admin_folder):
        login = AdminLoginPage(driver)
        login.open(base_url, admin_folder)
        login.login(admin_email, admin_password)

        dashboard = AdminDashboardPage(driver)
        dashboard.check_logged_in()

        products = AdminProductPage(driver)
        products.open_create_page(base_url, admin_folder)
        products.choose_standard_type()
        products.fill_product_form(name="Product To Delete", price="10.00", qty="5")
        products.save()
        assert products.delete()
