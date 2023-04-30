from selenium.webdriver.common.by import By

from pages.base_page import BasePage
from locators.user.userform_locators import UserFormLocators

user_information = {}


class DashboardUserFormPage(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def provide_main_and_billing_info(self, data, generated_password):
        self.set_value_into_element(UserFormLocators.username_locator, data['username'])
        self.set_value_into_element(UserFormLocators.password_locator, generated_password)
        self.set_value_into_element(UserFormLocators.repeat_password_locator, generated_password)
        self.set_value_into_element(UserFormLocators.account_name_locator, data['account_name'])
        self.set_value_into_element(UserFormLocators.email_locator, data['email'])
        self.set_value_into_element(UserFormLocators.contact_person_full_name_locator, data['contact_person_full_name'])
        self.set_value_into_element(UserFormLocators.contact_person_email_locator, data['contact_person_email'])
        self.set_value_into_element(UserFormLocators.contact_persona_phone_locator, data['contact_person_phone'])
        self.select_dropdown_value(UserFormLocators.country_label, data['country'])
        self.select_dropdown_value(UserFormLocators.company_label, data['company_name'])

    def provide_branding_info(self, data):
        self.select_dropdown_value(UserFormLocators.sales_manager_label, data['sales_manager'])
        self.select_dropdown_value(UserFormLocators.responsible_adops_label, data['responsible_adops'])
        self.select_dropdown_value(UserFormLocators.account_manager_label, data['account_manager'])

    def provide_currency_margin(self, data):
        self.select_dropdown_value(UserFormLocators.currency_label, data['currency'])
        self.set_value_into_element(UserFormLocators.min_bid_locator, data['min_bid'])
        self.set_value_into_element(UserFormLocators.max_bid_locator, data['max_bid'])
        self.set_value_into_element(UserFormLocators.tech_fee_locator, data['tech_fee'])

    def click_save_user_btn(self):
        self.click_on_element(UserFormLocators.save_button_locator)

    @staticmethod
    def reset_user_information():
        global user_information
        user_information = {'main_and_billing_info': {}, 'branding_info': {}, 'currency_margin': {}}

    def get_user_information(self):
        self.reset_user_information()
        user_information['main_and_billing_info']['username'] = self.get_element_text(UserFormLocators.username_locator,
                                                                                      input_tag=True)
        user_information['main_and_billing_info']['account_name'] = self.get_element_text(
            UserFormLocators.account_name_locator, input_tag=True)
        user_information['main_and_billing_info']['email'] = self.get_element_text(UserFormLocators.email_locator,
                                                                                   input_tag=True)
        user_information['main_and_billing_info']['contact_person_full_name'] = self.get_element_text(
            UserFormLocators.contact_person_full_name_locator, input_tag=True)
        user_information['main_and_billing_info']['contact_person_email'] = self.get_element_text(
            UserFormLocators.contact_person_email_locator, input_tag=True)
        user_information['main_and_billing_info']['contact_person_phone'] = self.get_element_text(
            UserFormLocators.contact_persona_phone_locator, input_tag=True)
        user_information['main_and_billing_info']['country'] = self.get_element_text(
            UserFormLocators.country_dropdown_locator)
        user_information['main_and_billing_info']['company_name'] = self.get_element_text(
            UserFormLocators.company_dropdown_locator)
        user_information['branding_info']['sales_manager'] = self.get_text_or_value_from_selected_option(
            UserFormLocators.sales_manager_label)
        user_information['branding_info']['responsible_adops'] = self.get_text_or_value_from_selected_option(
            UserFormLocators.responsible_adops_label)
        user_information['branding_info']['account_manager'] = self.get_text_or_value_from_selected_option(
            UserFormLocators.account_manager_label)
        user_information['currency_margin']['currency'] = self.get_element_text(
            UserFormLocators.currency_dropdown_locator)
        user_information['currency_margin']['currency_rate'] = self.get_element_text(
            UserFormLocators.currency_rate_locator, input_tag=True)
        user_information['currency_margin']['min_bid'] = self.get_element_text(UserFormLocators.min_bid_locator,
                                                                               input_tag=True)
        user_information['currency_margin']['max_bid'] = self.get_element_text(UserFormLocators.max_bid_locator,
                                                                               input_tag=True)
        user_information['currency_margin']['tech_fee'] = self.get_element_text(UserFormLocators.tech_fee_locator,
                                                                                input_tag=True)
        self.click_on_element(UserFormLocators.cancel_button_locator)
        return user_information

    def provide_and_save_user_information(self, user_data, generated_password):
        self.provide_main_and_billing_info(user_data['main_and_billing_info'], generated_password)
        self.provide_branding_info(user_data['branding_info'])
        self.provide_currency_margin(user_data['currency_margin'])
        self.click_save_user_btn()

    def check_uncheck_checkbox(self, checkbox_name, do_check):
        checkbox_locator = (By.XPATH, "//label[contains(text(),  '" + checkbox_name + "')]/..//input")
        element = self.wait_for_presence_of_element(checkbox_locator)
        if element.is_selected() != do_check:
            self.click_on_element(checkbox_locator)
