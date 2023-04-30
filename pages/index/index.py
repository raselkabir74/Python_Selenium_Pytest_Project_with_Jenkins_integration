from selenium.webdriver.common.keys import Keys
from locators.index.index_locator import IndexLocator
from pages.base_page import BasePage


class DspDashboardIndex(BasePage):

    def __init__(self, config, driver, env='stage'):
        super().__init__(driver)
        self.config = config
        self.env = env

    def login(self):
        if self.env == 'stage':
            self.driver.get(self.config['credential']['url'])
        else:
            self.driver.get(self.config['credential']['prod-url'])
        self.login_user(self.config['credential']['username'], self.config['credential']['password'])

    def login_user(self, login_username, login_password):
        self.set_value_into_element(IndexLocator.username_locator, login_username)
        self.set_value_into_element(IndexLocator.password_locator, login_password + Keys.ENTER)

    def get_page_title(self):
        return self.driver.title
