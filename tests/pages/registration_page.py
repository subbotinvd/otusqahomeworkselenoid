import allure
from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class RegistrationPage(BasePage):
    FORM = (By.ID, "customer-form")
    FIRSTNAME = (By.CSS_SELECTOR, "#customer-form input[name='firstname']")
    LASTNAME = (By.CSS_SELECTOR, "#customer-form input[name='lastname']")
    EMAIL = (By.CSS_SELECTOR, "#customer-form input[name='email']")
    PASSWORD = (By.CSS_SELECTOR, "#customer-form input[name='password']")
    GDPR_LABEL = (By.CSS_SELECTOR, "#customer-form label[for='field-psgdpr']")
    PRIVACY_LABEL = (By.CSS_SELECTOR, "#customer-form label[for='field-customer_privacy']")
    SUBMIT = (By.CSS_SELECTOR, "#customer-form .form-control-submit")
    USER_MENU = (By.ID, "userMenuButton")

    @allure.step("Open registration page")
    def open(self, base_url):
        self.logger.info("Opening registration page")
        super().open(f"{base_url}/registration")

    @allure.step("Check registration page elements")
    def check_elements(self):
        self.logger.info("Checking registration page elements")
        self.is_visible(*self.FORM)
        self.is_visible(*self.FIRSTNAME)
        self.is_visible(*self.LASTNAME)
        self.is_visible(*self.EMAIL)
        self.is_visible(*self.PASSWORD)
        self.is_visible(*self.SUBMIT)

    @allure.step("Register with email {email}")
    def register(self, firstname, lastname, email, password):
        self.logger.info("Registering user: %s", email)
        self.input_text(*self.FIRSTNAME, firstname)
        self.input_text(*self.LASTNAME, lastname)
        self.input_text(*self.EMAIL, email)
        self.input_text(*self.PASSWORD, password)
        self.click(*self.GDPR_LABEL)
        self.click(*self.PRIVACY_LABEL)
        self.click(*self.SUBMIT)

    @allure.step("Check registration success")
    def is_success(self):
        self.logger.info("Checking registration success")
        return self.is_visible(*self.USER_MENU)
