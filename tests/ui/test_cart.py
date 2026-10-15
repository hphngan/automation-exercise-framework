import pytest

from pages.cart_page import CartPage
from pages.products_page import ProductsPage
from utils.config import BASE_URL


pytestmark = pytest.mark.ui


def test_add_product_to_cart(browser):
    products = ProductsPage(browser, BASE_URL)
    cart = CartPage(browser, BASE_URL)

    products.open().add_product_to_cart(product_id=1).view_cart()

    assert cart.has_product(product_id=1)
    assert cart.product_name(product_id=1) == "Blue Top"


def test_remove_product_from_cart(browser):
    products = ProductsPage(browser, BASE_URL)
    cart = CartPage(browser, BASE_URL)

    products.open().add_product_to_cart(product_id=1).view_cart()
    cart.remove_product(product_id=1)

    assert cart.is_empty()


def test_verify_product_quantity(browser):
    products = ProductsPage(browser, BASE_URL)
    cart = CartPage(browser, BASE_URL)

    (
        products.open()
        .open_product_details(product_id=1)
        .set_quantity(4)
        .add_current_product_to_cart()
        .view_cart()
    )

    assert cart.quantity(product_id=1) == 4
