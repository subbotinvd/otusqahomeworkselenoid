import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class AdminLoginPage(BasePage):
    FORM = (By.ID, "login_form")
    EMAIL = (By.ID, "email")
    PASSWORD = (By.ID, "passwd")
    SUBMIT = (By.ID, "submit_login")

    @allure.step("Open admin login page")
    def open(self, base_url, admin_folder="admin"):
        self.logger.info("Opening admin login page")
        super().open(f"{base_url}/{admin_folder}/")

    @allure.step("Check admin login page elements")
    def check_elements(self):
        self.logger.info("Checking admin login page elements")
        self.is_visible(*self.FORM)
        self.is_visible(*self.EMAIL)
        self.is_visible(*self.PASSWORD)
        self.is_visible(*self.SUBMIT)

    @allure.step("Login to admin panel as {username}")
    def login(self, username, password):
        self.logger.info("Logging in as: %s", username)
        self.input_text(*self.EMAIL, username)
        self.input_text(*self.PASSWORD, password)
        self.click(*self.SUBMIT)
