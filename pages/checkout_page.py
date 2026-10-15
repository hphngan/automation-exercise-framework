from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class CheckoutPage(BasePage):
    ADDRESS_DETAILS = (By.XPATH, "//h2[normalize-space()='Address Details']")
    DELIVERY_ADDRESS = (By.ID, "address_delivery")
    ORDER_COMMENT = (By.NAME, "message")
    PLACE_ORDER = (By.CSS_SELECTOR, "a[href='/payment']")
    NAME_ON_CARD = (By.CSS_SELECTOR, "[data-qa='name-on-card']")
    CARD_NUMBER = (By.CSS_SELECTOR, "[data-qa='card-number']")
    CVC = (By.CSS_SELECTOR, "[data-qa='cvc']")
    EXPIRY_MONTH = (By.CSS_SELECTOR, "[data-qa='expiry-month']")
    EXPIRY_YEAR = (By.CSS_SELECTOR, "[data-qa='expiry-year']")
    PAY_BUTTON = (By.CSS_SELECTOR, "[data-qa='pay-button']")
    ORDER_PLACED = (By.CSS_SELECTOR, "[data-qa='order-placed']")
    CONFIRMATION_MESSAGE = (By.CSS_SELECTOR, ".col-sm-9 > p")

    def wait_until_loaded(self):
        self.find(self.ADDRESS_DETAILS)
        return self

    def delivery_address(self):
        return self.text(self.DELIVERY_ADDRESS)

    def enter_comment(self, comment):
        self.type(self.ORDER_COMMENT, comment)
        return self

    def place_order(self):
        self.click(self.PLACE_ORDER)
        self.wait.until(EC.url_contains("/payment"))
        self.find(self.NAME_ON_CARD)
        return self

    def pay(self, payment):
        self.type(self.NAME_ON_CARD, payment["name_on_card"])
        self.type(self.CARD_NUMBER, payment["card_number"])
        self.type(self.CVC, payment["cvc"])
        self.type(self.EXPIRY_MONTH, payment["expiry_month"])
        self.type(self.EXPIRY_YEAR, payment["expiry_year"])
        self.click(self.PAY_BUTTON)
        self.find(self.ORDER_PLACED)
        return self

    def order_was_placed(self):
        return self.text(self.ORDER_PLACED) == "ORDER PLACED!"

    def confirmation_message(self):
        return self.text(self.CONFIRMATION_MESSAGE)
