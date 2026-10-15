from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class SignupPage(BasePage):
    SIGNUP_NAME = (By.CSS_SELECTOR, "[data-qa='signup-name']")
    SIGNUP_EMAIL = (By.CSS_SELECTOR, "[data-qa='signup-email']")
    SIGNUP_BUTTON = (By.CSS_SELECTOR, "[data-qa='signup-button']")

    TITLE_MR = (By.ID, "id_gender1")
    TITLE_MRS = (By.ID, "id_gender2")
    PASSWORD = (By.CSS_SELECTOR, "[data-qa='password']")
    DAYS = (By.CSS_SELECTOR, "[data-qa='days']")
    MONTHS = (By.CSS_SELECTOR, "[data-qa='months']")
    YEARS = (By.CSS_SELECTOR, "[data-qa='years']")
    FIRST_NAME = (By.CSS_SELECTOR, "[data-qa='first_name']")
    LAST_NAME = (By.CSS_SELECTOR, "[data-qa='last_name']")
    COMPANY = (By.CSS_SELECTOR, "[data-qa='company']")
    ADDRESS = (By.CSS_SELECTOR, "[data-qa='address']")
    ADDRESS_2 = (By.CSS_SELECTOR, "[data-qa='address2']")
    COUNTRY = (By.CSS_SELECTOR, "[data-qa='country']")
    STATE = (By.CSS_SELECTOR, "[data-qa='state']")
    CITY = (By.CSS_SELECTOR, "[data-qa='city']")
    ZIPCODE = (By.CSS_SELECTOR, "[data-qa='zipcode']")
    MOBILE_NUMBER = (By.CSS_SELECTOR, "[data-qa='mobile_number']")
    CREATE_ACCOUNT = (By.CSS_SELECTOR, "[data-qa='create-account']")
    ACCOUNT_CREATED = (By.CSS_SELECTOR, "[data-qa='account-created']")
    CONTINUE_BUTTON = (By.CSS_SELECTOR, "[data-qa='continue-button']")
    LOGGED_IN_USER = (
        By.XPATH,
        "//div[contains(@class, 'shop-menu')]//a[contains(., 'Logged in as')]",
    )
    DELETE_ACCOUNT = (By.CSS_SELECTOR, "a[href='/delete_account']")
    ACCOUNT_DELETED = (By.CSS_SELECTOR, "[data-qa='account-deleted']")

    def open(self):
        return self.open_path("/login")

    def start_registration(self, name, email):
        self.type(self.SIGNUP_NAME, name)
        self.type(self.SIGNUP_EMAIL, email)
        self.click(self.SIGNUP_BUTTON)
        self.find(self.PASSWORD)
        return self

    def complete_registration(self, user):
        title = user.get("title", "Mr")
        self.click(self.TITLE_MRS if title in {"Mrs", "Miss"} else self.TITLE_MR)
        self.type(self.PASSWORD, user["password"])
        Select(self.find(self.DAYS)).select_by_value(str(user["birth_date"]))
        Select(self.find(self.MONTHS)).select_by_value(str(user["birth_month"]))
        Select(self.find(self.YEARS)).select_by_value(str(user["birth_year"]))
        self.type(self.FIRST_NAME, user["firstname"])
        self.type(self.LAST_NAME, user["lastname"])
        self.type(self.COMPANY, user["company"])
        self.type(self.ADDRESS, user["address1"])
        self.type(self.ADDRESS_2, user["address2"])
        Select(self.find(self.COUNTRY)).select_by_visible_text(user["country"])
        self.type(self.STATE, user["state"])
        self.type(self.CITY, user["city"])
        self.type(self.ZIPCODE, user["zipcode"])
        self.type(self.MOBILE_NUMBER, user["mobile_number"])
        self.click(self.CREATE_ACCOUNT)
        return self

    def register(self, user):
        self.open()
        self.start_registration(user["name"], user["email"])
        return self.complete_registration(user)

    def account_was_created(self):
        return self.text(self.ACCOUNT_CREATED) == "ACCOUNT CREATED!"

    def continue_to_account(self):
        account_created_url = self.driver.current_url
        self.click(self.CONTINUE_BUTTON)
        self.wait.until(EC.url_changes(account_created_url))
        self.find(self.LOGGED_IN_USER)
        return self

    def logged_in_as(self):
        return self.text(self.LOGGED_IN_USER).replace("Logged in as", "").strip()

    def delete_account(self):
        self.click(self.DELETE_ACCOUNT)
        return self.wait.until(EC.visibility_of_element_located(self.ACCOUNT_DELETED))
