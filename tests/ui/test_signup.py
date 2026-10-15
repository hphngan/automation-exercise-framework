import pytest

from pages.signup_page import SignupPage
from utils.config import BASE_URL


pytestmark = pytest.mark.ui


def test_register_new_account(browser, user_api, user_data):
    page = SignupPage(browser, BASE_URL)

    try:
        page.register(user_data)

        assert page.account_was_created()

        page.continue_to_account()
        assert page.logged_in_as() == user_data["name"]
    finally:
        user_api.delete_user(user_data["email"], user_data["password"])
