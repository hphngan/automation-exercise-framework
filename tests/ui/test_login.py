import pytest

from pages.login_page import LoginPage
from utils.config import BASE_URL


pytestmark = pytest.mark.ui


def test_valid_login(browser, created_user):
    page = LoginPage(browser, BASE_URL)

    page.open().login(created_user["email"], created_user["password"])

    assert page.logged_in_as() == created_user["name"]


def test_invalid_login(browser):
    page = LoginPage(browser, BASE_URL)

    page.open().login("unknown-ui-user@example.com", "wrong-password")

    assert page.error_message() == "Your email or password is incorrect!"
