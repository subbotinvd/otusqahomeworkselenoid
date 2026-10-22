import logging
import os

import allure
import pytest
from selenium import webdriver

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)


def pytest_addoption(parser):
    parser.addoption(
        "--browser",
        default="chrome",
        help="Browser to run tests: chrome or firefox",
    )
    parser.addoption(
        "--browser_version",
        default=os.getenv("BROWSER_VERSION"),
        help="Browser version on the remote executor (Selenoid)",
    )
    parser.addoption(
        "--url",
        default=os.getenv("SHOP_URL", "http://localhost:8080"),
        help="Base URL of the shop",
    )
    parser.addoption(
        "--executor",
        default=os.getenv("EXECUTOR"),
        help="Remote Selenium hub host, e.g. selenoid",
    )
    parser.addoption(
        "--headless",
        action="store_true",
        default=os.getenv("HEADLESS", "0") == "1",
        help="Run browser in headless mode (enabled by default in Docker)",
    )


@pytest.fixture(scope="session")
def browser(request):
    return request.config.getoption("--browser")


@pytest.fixture(scope="session")
def base_url(request):
    return request.config.getoption("--url").rstrip("/")


@pytest.fixture(scope="session")
def admin_folder():
    return os.getenv("ADMIN_FOLDER", "admin")


@pytest.fixture(scope="session")
def admin_email():
    return os.getenv("ADMIN_EMAIL", "admin@prestashop.com")


@pytest.fixture(scope="session")
def admin_password():
    return os.getenv("ADMIN_PASSWORD", "AdminDemo-2026-Pass")


@pytest.fixture(scope="function")
def driver(browser, request):
    headless = request.config.getoption("--headless")
    browser_version = request.config.getoption("--browser_version")
    executor = request.config.getoption("--executor")

    if browser == "chrome":
        options = webdriver.ChromeOptions()
        options.add_experimental_option(
            "prefs",
            {
                "credentials_enable_service": False,
                "profile.password_manager_enabled": False,
            },
        )
        if headless:
            options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--window-size=1920,1080")
    elif browser == "firefox":
        options = webdriver.FirefoxOptions()
        if headless:
            options.add_argument("--headless")
        options.add_argument("--width=1920")
        options.add_argument("--height=1080")
    else:
        raise ValueError(f"Unsupported browser: {browser}")

    if executor:
        options.set_capability("enableVNC", True)
        options.set_capability("screenResolution", "1920x1080")
        if browser_version:
            options.set_capability("browserVersion", browser_version)
        if "://" not in executor:
            executor = f"http://{executor}"
        if ":" not in executor.split("//")[-1]:
            executor = f"{executor}:4444"
        if not executor.endswith("/wd/hub"):
            executor = f"{executor}/wd/hub"
        drv = webdriver.Remote(command_executor=executor, options=options)
    elif browser == "chrome":
        drv = webdriver.Chrome(options=options)
    else:
        drv = webdriver.Firefox(options=options)

    drv.implicitly_wait(5)
    yield drv
    drv.quit()


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        drv = item.funcargs.get("driver")
        if drv:
            allure.attach(
                drv.get_screenshot_as_png(),
                name="screenshot_on_failure",
                attachment_type=allure.attachment_type.PNG,
            )
