from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class ProductsPage(BasePage):
    PAGE_TITLE = (By.CSS_SELECTOR, ".features_items h2.title")
    SEARCH_INPUT = (By.ID, "search_product")
    SEARCH_BUTTON = (By.ID, "submit_search")
    PRODUCT_NAMES = (By.CSS_SELECTOR, ".features_items .productinfo > p")
    PRODUCT_DETAIL_NAME = (By.CSS_SELECTOR, ".product-information h2")
    PRODUCT_INFORMATION = (By.CSS_SELECTOR, ".product-information")
    QUANTITY = (By.ID, "quantity")
    DETAIL_ADD_TO_CART = (By.CSS_SELECTOR, ".product-information button.cart")
    CART_MODAL = (By.ID, "cartModal")
    VIEW_CART = (By.CSS_SELECTOR, "#cartModal a[href='/view_cart']")

    def open(self):
        self.open_path("/products")
        self.find(self.PAGE_TITLE)
        return self

    def search(self, query):
        self.type(self.SEARCH_INPUT, query)
        self.click(self.SEARCH_BUTTON)
        self.wait.until(EC.url_contains("/products?search="))
        self.find(self.PAGE_TITLE)
        return self

    def product_names(self):
        return [element.text.strip() for element in self.find_all(self.PRODUCT_NAMES)]

    def open_product_details(self, product_id=1):
        self.click((By.CSS_SELECTOR, f"a[href='/product_details/{product_id}']"))
        self.wait.until(EC.url_contains(f"/product_details/{product_id}"))
        self.find(self.PRODUCT_INFORMATION)
        return self

    def product_name(self):
        return self.text(self.PRODUCT_DETAIL_NAME)

    def product_information(self):
        return self.text(self.PRODUCT_INFORMATION)

    def add_product_to_cart(self, product_id=1):
        self.click(
            (
                By.CSS_SELECTOR,
                f".productinfo a.add-to-cart[data-product-id='{product_id}']",
            )
        )
        self.wait.until(EC.visibility_of_element_located(self.CART_MODAL))
        return self

    def set_quantity(self, quantity):
        self.type(self.QUANTITY, str(quantity))
        return self

    def add_current_product_to_cart(self):
        self.click(self.DETAIL_ADD_TO_CART)
        self.wait.until(EC.visibility_of_element_located(self.CART_MODAL))
        return self

    def view_cart(self):
        self.click(self.VIEW_CART)
        self.wait.until(EC.url_contains("/view_cart"))
        return self
