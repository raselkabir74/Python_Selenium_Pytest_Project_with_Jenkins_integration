from selenium.webdriver.common.by import By


class IndexLocator:
    # [Start] locators
    username_locator = (By.XPATH, "//input[@id='username']")
    password_locator = (By.XPATH, "//input[@id='password']")
    # [End] locators
