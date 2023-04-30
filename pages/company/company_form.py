from pages.base_page import BasePage
from locators.company.company_form_locators import CompanyFormLocators

company_information = {}


class DashboardCompanyForm(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def provide_and_save_company_information(self, company_data, mode='add'):
        self.set_value_into_element(CompanyFormLocators.company_name_locator, company_data['name'])
        self.select_dropdown_value(CompanyFormLocators.country_label, company_data['country'])
        self.set_value_into_element(CompanyFormLocators.company_address_textarea_locator, company_data['address'])
        self.set_value_into_element(CompanyFormLocators.company_registration_number_locator, company_data['reg_number'])
        self.set_value_into_element(CompanyFormLocators.company_vat_id_locator, company_data['vat_id'])
        self.set_value_into_element(CompanyFormLocators.company_financial_contact_name_locator,
                                    company_data['finance_contact_name'])
        self.set_value_into_element(CompanyFormLocators.company_financial_contact_email_locator,
                                    company_data['finance_contact_email'])
        self.set_value_into_element(CompanyFormLocators.company_financial_phone_number_locator,
                                    company_data['finance_phone_number'])
        self.set_value_into_element(CompanyFormLocators.company_payment_term_locator, company_data['payment_term'])
        if mode == 'add':
            self.select_dropdown_value(CompanyFormLocators.client_tier_label, company_data['client_tier'])
        self.set_value_into_element(CompanyFormLocators.company_discount_locator, company_data['discount'])
        self.set_value_into_element(CompanyFormLocators.company_bonus_locator, company_data['bonus'])
        self.set_value_into_element(CompanyFormLocators.company_tax_locator, company_data['tax'])
        self.select_dropdown_value(CompanyFormLocators.collection_person_label, company_data['collection_person'])
        self.click_on_element(CompanyFormLocators.save_button_locator)

    def get_company_information(self):
        global company_information
        company_information['name'] = self.get_element_text(CompanyFormLocators.company_name_locator, input_tag=True)
        company_information['country'] = self.get_element_text(CompanyFormLocators.country_dropdown_locator)
        company_information['address'] = self.get_element_text(CompanyFormLocators.company_address_textarea_locator)
        company_information['reg_number'] = self.get_element_text(
            CompanyFormLocators.company_registration_number_locator, input_tag=True)
        company_information['vat_id'] = self.get_element_text(CompanyFormLocators.company_vat_id_locator,
                                                              input_tag=True)
        company_information['finance_contact_name'] = self.get_element_text(
            CompanyFormLocators.company_financial_contact_name_locator, input_tag=True)
        company_information['finance_contact_email'] = self.get_element_text(
            CompanyFormLocators.company_financial_contact_email_locator, input_tag=True)
        company_information['finance_phone_number'] = self.get_element_text(
            CompanyFormLocators.company_financial_phone_number_locator, input_tag=True)
        company_information['payment_term'] = self.get_element_text(CompanyFormLocators.company_payment_term_locator,
                                                                    input_tag=True)
        company_information['client_tier'] = self.get_element_text(CompanyFormLocators.client_tier_dropdown_locator)
        company_information['discount'] = self.get_element_text(CompanyFormLocators.company_discount_locator,
                                                                input_tag=True)
        company_information['bonus'] = self.get_element_text(CompanyFormLocators.company_bonus_locator, input_tag=True)
        company_information['tax'] = self.get_element_text(CompanyFormLocators.company_tax_locator, input_tag=True)
        company_information['collection_person'] = self.get_element_text(
            CompanyFormLocators.collection_person_dropdown_locator)
        self.click_on_element(CompanyFormLocators.cancel_button_locator)
        return company_information
