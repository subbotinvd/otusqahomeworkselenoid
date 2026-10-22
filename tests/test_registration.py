import time

import allure

from pages.registration_page import RegistrationPage


@allure.feature("User Registration")
class TestRegistration:

    @allure.story("New User")
    @allure.title("Register new user")
    def test_register_new_user(self, driver, base_url):
        timestamp = int(time.time())
        page = RegistrationPage(driver)
        page.open(base_url)
        page.register(
            firstname="Test",
            lastname="User",
            email=f"test.user{timestamp}@example.com",
            password=f"Qa-pass-{timestamp}",
        )
        assert page.is_success()
