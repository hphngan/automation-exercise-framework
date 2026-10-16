import pytest

from pages.products_page import ProductsPage
from utils.config import BASE_URL


pytestmark = pytest.mark.ui


def test_search_product(browser):
    page = ProductsPage(browser, BASE_URL)

    page.open().search("Blue Top")

    names = page.product_names()
    assert names
    assert all("blue top" in name.lower() for name in names)


def test_open_product_details(browser):
    page = ProductsPage(browser, BASE_URL)

    page.open().open_product_details(product_id=1)

    # assert page.product_name() == "Blue Top"
    
    # This assertion is intentionally incorrect to demonstrate a failing test
    assert page.product_name() == "Wrong Product Name"  
    
    details = page.product_information()
    assert "Category: Women > Tops" in details
    assert "Availability: In Stock" in details
    assert "Condition: New" in details
    assert "Brand:" in details
    assert "Polo" in details
