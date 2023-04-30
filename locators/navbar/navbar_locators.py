from selenium.webdriver.common.by import By


class NavbarLocators:
    # [Start] locators
    account_dropdown_locator = (By.XPATH, "//a[@id='navAccountsDropdown']")
    search_box_locator = (By.XPATH, "//input[@title='Search' and @class='fixed_search']")
    three_dot_locator = (By.XPATH, "//a[@id='navSettingsMenu']/i")
    logout_locator = (By.XPATH, "//a[normalize-space()='Log out']")
    login_as_locator = (By.XPATH, "//a[contains(text(), 'Log in as')]")
    logout_as_locator = (By.XPATH, "//a[contains(text(), 'Log out as')]")
    # [End] locators
