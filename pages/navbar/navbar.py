from selenium.webdriver.common.keys import Keys
from pages.base_page import BasePage
from locators.navbar.navbar_locators import NavbarLocators


class DashboardNavbar(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def impersonate_user(self, name):
        self.click_on_element(NavbarLocators.account_dropdown_locator)
        self.set_value_into_element(NavbarLocators.search_box_locator, name + Keys.ENTER)

    def login_as(self, user_name):
        self.impersonate_user(user_name)
        self.click_on_element(NavbarLocators.three_dot_locator)
        self.click_on_element(NavbarLocators.login_as_locator)

    def logout_as(self):
        self.click_on_element(NavbarLocators.three_dot_locator)
        self.click_on_element(NavbarLocators.logout_as_locator)

    def logout_user(self):
        self.click_on_element(NavbarLocators.three_dot_locator)
        self.click_on_element(NavbarLocators.logout_locator)