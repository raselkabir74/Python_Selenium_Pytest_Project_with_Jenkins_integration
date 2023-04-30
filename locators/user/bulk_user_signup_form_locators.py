from selenium.webdriver.common.by import By


class BulkUserSignUpFormLocators:
    # [Start] locators
    password_locator = (By.XPATH, "//input[@id='password']")
    repeat_password_locator = (By.XPATH, "//input[@id='password_confirmation']")
    account_name_locator = (By.XPATH, "//input[@id='account_name']")
    contact_person_full_name_locator = (By.XPATH, "//input[@id='contact_person_full_name']")
    contact_person_phone_locator = (By.XPATH, "//input[@id='contact_person_phone']")
    submit_button_locator = (By.XPATH, "//button[@id='submitBtn']")
    login_button_locator = (By.XPATH, "//a[normalize-space()='Login']")
    # [End] locators
