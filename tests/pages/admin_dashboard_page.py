import allure
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from pages.base_page import BasePage


class AdminDashboardPage(BasePage):
    SHOP_VERSION = (By.ID, "shop_version")
    EMPLOYEE_MENU = (By.CSS_SELECTOR, "#header_infos #header-employee-container")
    EMPLOYEE_MENU_LEGACY = (By.ID, "employee_infos")
    LOGOUT = (By.CSS_SELECTOR, "a#header_logout")

    @allure.step("Check admin is logged in")
    def check_logged_in(self):
        self.logger.info("Checking admin is logged in")
        self.is_visible(*self.SHOP_VERSION)

    @allure.step("Logout from admin panel")
    def logout(self):
        self.logger.info("Logging out from admin panel")
        self._open_employee_menu()
        self.click(*self.LOGOUT)

    def _open_employee_menu(self):
        for _ in range(3):
            self.click_any(self.EMPLOYEE_MENU, self.EMPLOYEE_MENU_LEGACY)
            try:
                WebDriverWait(self.driver, 2).until(
                    EC.visibility_of_element_located(self.LOGOUT)
                )
                return
            except TimeoutException:
                continue
        raise TimeoutException("Employee menu dropdown did not open")
