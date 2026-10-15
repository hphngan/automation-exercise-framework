from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class CartPage(BasePage):
    CART_TABLE = (By.ID, "cart_info_table")
    EMPTY_CART = (By.CSS_SELECTOR, "#empty_cart")
    PROCEED_TO_CHECKOUT = (By.CSS_SELECTOR, "a.check_out")

    def open(self):
        return self.open_path("/view_cart")

    @staticmethod
    def _row(product_id):
        return (By.ID, f"product-{product_id}")

    def product_name(self, product_id):
        return self.text(
            (By.CSS_SELECTOR, f"#product-{product_id} .cart_description h4 a")
        )

    def quantity(self, product_id):
        return int(
            self.text((By.CSS_SELECTOR, f"#product-{product_id} .cart_quantity button"))
        )

    def has_product(self, product_id):
        return self.is_visible(self._row(product_id))

    def remove_product(self, product_id):
        row = self.find(self._row(product_id))
        self.click(
            (By.CSS_SELECTOR, f"#product-{product_id} .cart_quantity_delete")
        )
        self.wait.until(EC.staleness_of(row))
        return self

    def is_empty(self):
        return self.is_visible(self.EMPTY_CART)

    def proceed_to_checkout(self):
        self.click(self.PROCEED_TO_CHECKOUT)
        self.wait.until(EC.url_contains("/checkout"))
        return self
