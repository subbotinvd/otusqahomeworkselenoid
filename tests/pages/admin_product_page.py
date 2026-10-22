import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class AdminProductPage(BasePage):

    GRID = (By.ID, "product_grid_table")
    NEW_PRODUCT_BUTTON = (By.ID, "page-header-desc-configuration-add")

    CREATE_FORM = (By.ID, "create_product")
    STANDARD_TYPE = (
        By.CSS_SELECTOR,
        "#create_product div.product-type-choices "
        "button.product-type-choice[data-value='standard']",
    )
    CREATE_BUTTON = (By.ID, "create_product_create")

    NAME_INPUT = (By.CSS_SELECTOR, "#product_header_name div.js-locale-en input")
    PRICING_TAB = (By.ID, "product_pricing-tab-nav")
    PRICE_INPUT = (By.ID, "product_pricing_retail_price_price_tax_excluded")
    STOCK_TAB = (By.ID, "product_stock-tab-nav")
    QUANTITY_INPUT = (By.ID, "product_stock_quantities_delta_quantity_delta")
    SAVE_BUTTON = (By.ID, "product_footer_save")
    ACTIONS_DROPDOWN = (By.ID, "product_footer_actions_dropdown")
    DELETE_ACTION = (By.ID, "product_footer_actions_delete")
    DELETE_CONFIRM = (
        By.CSS_SELECTOR,
        "#delete-product-footer-modal button.btn-confirm-submit",
    )

    GROWL_MESSAGE = (By.CSS_SELECTOR, "#growls .growl-message")

    @allure.step("Open products list page")
    def open_products(self, base_url, admin_folder="admin"):
        self.logger.info("Opening products list page")
        super().open(f"{base_url}/{admin_folder}/index.php/sell/catalog/products")
        self.is_visible(*self.GRID)

    @allure.step("Check products list page elements")
    def check_products_list(self):
        self.logger.info("Checking products list page elements")
        self.is_visible(*self.GRID)
        self.is_visible(*self.NEW_PRODUCT_BUTTON)

    @allure.step("Open new product page")
    def open_create_page(self, base_url, admin_folder="admin"):
        self.logger.info("Opening new product page")
        url = f"{base_url}/{admin_folder}/index.php/sell/catalog/products/create"
        super().open(url)
        self.is_visible(*self.CREATE_FORM)

    @allure.step("Choose standard product type")
    def choose_standard_type(self):
        self.logger.info("Choosing standard product type")
        self.click(*self.STANDARD_TYPE)
        self.click(*self.CREATE_BUTTON)
        self.is_visible(*self.NAME_INPUT)

    @allure.step("Fill product form: name={name}, price={price}, qty={qty}")
    def fill_product_form(self, name, price, qty):
        self.logger.info("Filling product form: %s", name)
        self.input_text(*self.NAME_INPUT, name)
        self.click(*self.PRICING_TAB)
        self.input_text(*self.PRICE_INPUT, price)
        self.click(*self.STOCK_TAB)
        self.input_text(*self.QUANTITY_INPUT, qty)

    @allure.step("Save product")
    def save(self):
        self.logger.info("Saving product")
        self.click(*self.SAVE_BUTTON)
        return self._wait_notification("Successful")

    @allure.step("Delete product")
    def delete(self):
        self.logger.info("Deleting product")
        self.click(*self.ACTIONS_DROPDOWN)
        self.click(*self.DELETE_ACTION)
        self.click(*self.DELETE_CONFIRM)
        return self._wait_notification("Successful deletion")

    def _wait_notification(self, text):
        return WebDriverWait(self.driver, 20).until(
            EC.text_to_be_present_in_element(self.GROWL_MESSAGE, text)
        )
