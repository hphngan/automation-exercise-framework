import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.config import BASE_URL


pytestmark = pytest.mark.ui


def test_checkout_displays_delivery_address(browser, created_user):
    LoginPage(browser, BASE_URL).open().login(
        created_user["email"],
        created_user["password"],
    )
    ProductsPage(browser, BASE_URL).open().add_product_to_cart(1).view_cart()

    CartPage(browser, BASE_URL).proceed_to_checkout()
    checkout = CheckoutPage(browser, BASE_URL).wait_until_loaded()

    address = checkout.delivery_address()
    assert created_user["firstname"] in address
    assert created_user["lastname"] in address
    assert created_user["address1"] in address
    assert created_user["city"] in address
    assert created_user["country"] in address
