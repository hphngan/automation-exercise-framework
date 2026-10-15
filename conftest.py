import os
import base64
import re
import warnings
from pathlib import Path
from uuid import uuid4

import pytest
import pytest_html
from selenium import webdriver

from api.api_client import APIClient
from api.product_api import ProductAPI
from api.user_api import UserAPI
from utils.config import BASE_URL
from utils.data_generator import generate_user_data


def pytest_collection_modifyitems(items):
    for item in items:
        if Path(str(item.path)).parent == Path(__file__).parent / "tests" / "api":
            item.add_marker(pytest.mark.api)


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    driver = item.funcargs.get("browser")
    if not report.failed or driver is None or report.when == "teardown":
        return

    try:
        screenshot = driver.get_screenshot_as_base64()
        directory = Path(item.config.rootpath) / "screenshots"
        directory.mkdir(parents=True, exist_ok=True)
        name = re.sub(r"[^a-zA-Z0-9_-]", "_", item.nodeid)[-160:]
        path = directory / f"{name}_{report.when}_{uuid4().hex[:8]}.png"
        path.write_bytes(base64.b64decode(screenshot))
        extras = getattr(report, "extras", [])
        extras.append(pytest_html.extras.png(screenshot, name="Failure screenshot"))
        report.extras = extras
    except Exception as exc:
        warnings.warn(f"Could not capture failure screenshot: {exc}", stacklevel=2)


def pytest_addoption(parser):
    ui_group = parser.getgroup("ui")
    ui_group.addoption(
        "--browser",
        action="store",
        choices=("chrome", "firefox"),
        default=os.getenv("UI_BROWSER", "chrome"),
        help="Browser used for UI tests (default: chrome).",
    )
    ui_group.addoption(
        "--headed",
        action="store_true",
        default=False,
        help="Show the browser window instead of running headlessly.",
    )


@pytest.fixture(scope="session")
def api_client():
    return APIClient(BASE_URL)


@pytest.fixture(scope="session")
def product_api(api_client):
    return ProductAPI(api_client)


@pytest.fixture(scope="session")
def user_api(api_client):
    return UserAPI(api_client)


@pytest.fixture
def user_data():
    return generate_user_data()


@pytest.fixture
def created_user(user_api, user_data):
    response = user_api.create_user(user_data)
    payload = response.json()
    assert response.status_code == 200
    assert payload["responseCode"] == 201, payload

    yield user_data

    # Cleanup is intentionally idempotent from the test suite's perspective.
    # A delete test may already have removed this account.
    user_api.delete_user(user_data["email"], user_data["password"])


@pytest.fixture
def browser(request):
    browser_name = request.config.getoption("--browser")
    headed = request.config.getoption("--headed")

    if browser_name == "firefox":
        options = webdriver.FirefoxOptions()
        options.page_load_strategy = "eager"
        if not headed:
            options.add_argument("-headless")
        driver = webdriver.Firefox(options=options)
    else:
        options = webdriver.ChromeOptions()
        options.page_load_strategy = "eager"
        if not headed:
            options.add_argument("--headless=new")
        options.add_argument("--window-size=1440,1000")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--no-sandbox")
        driver = webdriver.Chrome(options=options)
        driver.execute_cdp_cmd("Network.enable", {})
        driver.execute_cdp_cmd(
            "Network.setBlockedURLs",
            {
                "urls": [
                    "*://*.doubleclick.net/*",
                    "*://*.googleadservices.com/*",
                    "*://*.googlesyndication.com/*",
                ]
            },
        )

    driver.set_page_load_timeout(30)
    if headed:
        driver.maximize_window()

    yield driver

    driver.quit()
