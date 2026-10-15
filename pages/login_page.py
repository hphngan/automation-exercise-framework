from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class LoginPage(BasePage):
    LOGIN_EMAIL = (By.CSS_SELECTOR, "[data-qa='login-email']")
    LOGIN_PASSWORD = (By.CSS_SELECTOR, "[data-qa='login-password']")
    LOGIN_BUTTON = (By.CSS_SELECTOR, "[data-qa='login-button']")
    LOGIN_ERROR = (By.CSS_SELECTOR, ".login-form form p")
    LOGGED_IN_USER = (
        By.XPATH,
        "//div[contains(@class, 'shop-menu')]//a[contains(., 'Logged in as')]",
    )

    def open(self):
        return self.open_path("/login")

    def login(self, email, password):
        self.type(self.LOGIN_EMAIL, email)
        self.type(self.LOGIN_PASSWORD, password)
        self.click(self.LOGIN_BUTTON)
        return self

    def error_message(self):
        return self.text(self.LOGIN_ERROR)

    def logged_in_as(self):
        return self.text(self.LOGGED_IN_USER).replace("Logged in as", "").strip()
