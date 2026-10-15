import pytest

from pages.cart_page import CartPage
from pages.checkout_page import CheckoutPage
from pages.login_page import LoginPage
from pages.products_page import ProductsPage
from utils.config import BASE_URL
from utils.data_generator import generate_payment_data


pytestmark = pytest.mark.e2e


def test_complete_checkout_and_verify_order_confirmation(browser, created_user):
    LoginPage(browser, BASE_URL).open().login(
        created_user["email"],
        created_user["password"],
    )

    products = ProductsPage(browser, BASE_URL)
    (
        products.open()
        .open_product_details(product_id=1)
        .set_quantity(2)
        .add_current_product_to_cart()
        .view_cart()
    )

    cart = CartPage(browser, BASE_URL)
    assert cart.product_name(product_id=1) == "Blue Top"
    assert cart.quantity(product_id=1) == 2
    cart.proceed_to_checkout()

    checkout = CheckoutPage(browser, BASE_URL)
    (
        checkout.wait_until_loaded()
        .enter_comment("Automated Selenium checkout")
        .place_order()
        .pay(generate_payment_data())
    )

    assert checkout.order_was_placed()
    assert "order has been confirmed" in checkout.confirmation_message().lower()
