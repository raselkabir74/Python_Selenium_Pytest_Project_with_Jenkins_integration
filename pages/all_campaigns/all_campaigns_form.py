from selenium.webdriver.common.keys import Keys
from locators.all_campaigns.all_campaign_locators import AllCampaignFormLocators
from pages.base_page import BasePage
from urllib.parse import urlparse
from urllib.parse import parse_qs


class DashboardAllCampaignForm(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def wait_for_loading(self):
        try:
            self.wait_for_visibility_of_element(AllCampaignFormLocators.processing_locator,
                                                time_out=self.FIVE_SEC_DELAY)
        except:
            self.wait_for_element_to_be_invisible(AllCampaignFormLocators.processing_locator)
        self.wait_for_element_to_be_invisible(AllCampaignFormLocators.processing_locator)

    def get_status_verification(self, status_name):
        self.wait_for_visibility_of_element(AllCampaignFormLocators.table_row_status_xpath.format(status_name),
                                            locator_initialization=True)
        return True

    def change_status_filter(self, status_name):
        self.dropdown_selection(AllCampaignFormLocators.status_filter_xpath, status_name)

    def change_user_filter(self, user_name):
        self.dropdown_selection(AllCampaignFormLocators.user_filter_xpath, user_name)

    def change_country_filter(self, country_name):
        self.dropdown_selection(AllCampaignFormLocators.country_filter_xpath, country_name)

    def all_statuses_verification(self, statuses):
        for status in statuses:
            if status == 'Pending':
                self.wait_for_loading()
                self.get_status_verification(status)
            else:
                self.change_status_filter(status)
                self.wait_for_loading()
                self.get_status_verification(status)
        return True

    def user_filter_verification(self, user_name):
        self.change_user_filter(user_name)
        self.wait_for_loading()
        self.change_status_filter('All')
        self.wait_for_loading()
        user_id = self.get_url_function(
            self.wait_for_visibility_of_element(AllCampaignFormLocators.table_row_login_as_xpath.format(user_name),
                                                locator_initialization=True).get_attribute('href'),
            parameter_name='admin_id')
        url_function = self.get_url_function(
            self.wait_for_visibility_of_element(AllCampaignFormLocators.table_row_login_as_xpath.format(user_name),
                                                locator_initialization=True).get_attribute('href'))
        method_name = self.get_url_function(
            self.wait_for_visibility_of_element(AllCampaignFormLocators.table_row_login_as_xpath.format(user_name),
                                                locator_initialization=True).get_attribute('href'),
            parameter_name='method')
        if user_id == '7722' and url_function == 'campaigns' and method_name == 'settings':
            return True
        else:
            return False

    def country_filter_verification(self, country_name):
        self.change_country_filter(country_name)
        self.wait_for_loading()
        self.change_user_filter('AutomationAdminUser')
        self.wait_for_loading()
        self.change_status_filter('All')
        self.wait_for_loading()
        self.wait_for_visibility_of_element(AllCampaignFormLocators.table_row_country_xpath.format(country_name),
                                            locator_initialization=True)
        return True

    def change_type_filter(self, type_name):
        self.dropdown_selection(AllCampaignFormLocators.type_filter_xpath, type_name)

    def get_type_verification(self, type_name):
        self.wait_for_visibility_of_element(AllCampaignFormLocators.table_row_type_xpath.format(type_name),
                                            locator_initialization=True)
        return True

    def all_type_verification(self, type_names):
        self.change_status_filter('All')
        self.wait_for_loading()
        for type_name in type_names:
            self.change_type_filter(type_name)
            self.wait_for_loading()
            self.get_type_verification(type_name)
        return True

    def change_last_approved_filter(self, user_name):
        self.dropdown_selection(AllCampaignFormLocators.last_approved_filter_xpath, user_name)

    def last_approved_by_verification(self, user_name):
        self.change_status_filter('All')
        self.wait_for_loading()
        self.change_last_approved_filter(user_name)
        self.wait_for_loading()
        self.wait_for_visibility_of_element(AllCampaignFormLocators.table_row_last_approved_by_xpath.format(user_name),
                                            locator_initialization=True)
        return True

    def search_verification(self, search_text):
        self.change_status_filter('All')
        self.wait_for_loading()
        self.change_user_filter('AutomationAdminUser')
        self.wait_for_loading()
        self.set_value_into_element(AllCampaignFormLocators.search_filter_locator, search_text + Keys.ENTER)
        self.wait_for_loading()
        url_function = self.get_url_function(self.wait_for_visibility_of_element(
            AllCampaignFormLocators.table_row_campaign_name_xpath.format(search_text),
            locator_initialization=True).get_attribute('href'))
        method_name = self.get_url_function(self.wait_for_visibility_of_element(
            AllCampaignFormLocators.table_row_campaign_name_xpath.format(search_text),
            locator_initialization=True).get_attribute('href'), parameter_name='method')
        if url_function == 'acampaigns' and method_name == 'view':
            return True
        else:
            return False

    def verify_three_dot_options(self, user_name):
        url_functions = []
        self.change_status_filter('All')
        self.wait_for_loading()
        self.change_user_filter(user_name)
        self.wait_for_loading()
        self.click_on_element(AllCampaignFormLocators.three_dot_locator)
        url_functions.append(self.get_url_function(
            self.wait_for_visibility_of_element(AllCampaignFormLocators.targeting_optimization_locator).get_attribute(
                'href')))
        url_functions.append(self.get_url_function(
            self.wait_for_visibility_of_element(AllCampaignFormLocators.view_report_locator).get_attribute(
                'href')))
        url_functions.append(self.get_url_function(
            self.wait_for_visibility_of_element(AllCampaignFormLocators.confirm_campaign_locator).get_attribute(
                'href')))
        url_functions.append(self.get_url_function(
            self.wait_for_visibility_of_element(AllCampaignFormLocators.reject_campaign_locator).get_attribute(
                'href')))
        url_functions.append(self.get_url_function(
            self.wait_for_visibility_of_element(AllCampaignFormLocators.delete_campaign_locator).get_attribute(
                'data-url'), parameter_name='method'))
        url_functions.append(self.get_url_function(self.wait_for_visibility_of_element(
            AllCampaignFormLocators.remove_completely_campaign_locator).get_attribute(
            'data-url'), parameter_name='remove'))
        return url_functions

    @staticmethod
    def get_url_function(url, parameter_name='function'):
        parsed_url = urlparse(url)
        captured_value = parse_qs(parsed_url.query)[parameter_name][0]
        return captured_value

    def clear_all(self):
        self.click_on_element(AllCampaignFormLocators.clear_all_locator)
        self.wait_for_loading()
