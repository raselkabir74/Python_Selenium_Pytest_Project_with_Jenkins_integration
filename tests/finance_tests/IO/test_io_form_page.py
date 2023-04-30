import copy
import json
import os
import time

import pytest
from selenium.webdriver import Keys

from configurations import generic_modules
from locators.company.company_form_locators import CompanyFormLocators
from locators.io.invoice_form_locator import InvoiceFormLocators
from locators.io.io_form_locator import IoFormLocators
from locators.io.io_list_locator import IoListLocators
from locators.user.userform_locators import UserFormLocators
from pages.io.io_form import DspDashboardIoForm
from pages.io.io_list import DspDashboardIoList
from pages.navbar.navbar import DashboardNavbar
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.user.user_form import DashboardUserFormPage
from utils.compare import CompareUtils as CompareUtil
from utils.currency import CurrencyUtils
from utils.io import IoUtils

date_format = "%d %b, %Y"
all_data_verification_message = "All data verification is successful"

@pytest.mark.skipif("JENKINS_URL" in os.environ, reason="Test need to be run manually")
def test_io_form_page(login_by_user_type):
    config, driver = login_by_user_type
    io_form_page = DspDashboardIoForm(driver)
    io_list_page = DspDashboardIoList(driver)
    sidebar_navigation = DashboardSidebarPage(driver)

    # PROVIDED IO DATA IN GUI
    global date_format, all_data_verification_message
    with open('assets/io/io_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = io_data['io_main_information'][
                                                     'io_title'] + generic_modules.get_random_string(5)

    # GETTING AND STORING INFO
    with open('assets/io/profile_finance_status_data.json') as json_file:
        profile_finance_status_data = json.load(json_file)
    pulled_profile_finance_status_data_from_gui = copy.deepcopy(profile_finance_status_data)

    company_profile_url = config['credential']['url'] + profile_finance_status_data['profile_finance_data'][
        'company_profile_url']
    driver.get(company_profile_url)
    profile_finance_status_data['profile_finance_data']['discount'] = io_form_page.get_element_text(
        CompanyFormLocators.company_discount_locator, input_tag=True) + "%"
    profile_finance_status_data['profile_finance_data']['bonus'] = io_form_page.get_element_text(
        CompanyFormLocators.company_bonus_locator, input_tag=True) + "%"
    profile_finance_status_data['profile_finance_data']['tax'] = io_form_page.get_element_text(
        CompanyFormLocators.company_bonus_locator, input_tag=True) + "%(i.e. WHT)"
    profile_finance_status_data['profile_finance_data'][
        'last_payment'] = io_form_page.get_current_date_with_specific_format(date_format)
    profile_finance_status_data['profile_finance_data'][
        'last_invoice'] = io_form_page.get_current_date_with_specific_format(date_format)

    generic_modules.step_info(
        "[START - RTB-6610] Validate whether the user is not able to create IO without filling up the mandatory fields")
    sidebar_navigation.navigate_to_io()
    io_list_page.navigate_to_add_io()
    io_form_page.click_on_element(IoFormLocators.date_field_locator)
    io_form_page.wait_for_presence_of_element(IoFormLocators.date_field_locator).send_keys(Keys.COMMAND + 'a')
    time.sleep(io_form_page.ONE_SEC_DELAY)
    io_form_page.wait_for_presence_of_element(IoFormLocators.date_field_locator).send_keys(Keys.DELETE)
    time.sleep(io_form_page.ONE_SEC_DELAY)
    io_form_page.set_value_into_specific_input_field(IoFormLocators.date_label, " ", tab_out=True)
    time.sleep(io_form_page.ONE_SEC_DELAY)
    io_form_page.click_on_element(IoFormLocators.save_and_generate_io_button_locator)
    assert True is io_form_page.is_element_present(IoFormLocators.define_missing_fields_warning_message_locator)
    io_form_page.click_on_specific_button(IoFormLocators.close_label)
    generic_modules.step_info(
        "[END - RTB-6610] Validate whether the user is not able to create IO without filling up the mandatory fields")

    generic_modules.step_info(
        "[START - RTB-6611] Validate whether the user is able to generate IO just by filling up the mandatory fields \n"
        "[START - RTB-6609] Validate Profile finance status are available in the io form page")
    io_creation_url = config['credential']['url'] + config['io-creation-page']['io-creation-url']
    driver.get(io_creation_url)
    io_form_page.provide_io_main_information(io_data)
    io_form_page.set_value_into_specific_input_field(IoFormLocators.date_label,
                                                     io_form_page.get_current_date_with_specific_format("%d %b, %Y"),
                                                     tab_out=True)
    io_form_page.provide_io_client_profile_info(io_data)
    io_form_page.click_on_element(IoFormLocators.save_and_generate_io_button_locator)
    io_url = driver.current_url
    assert "Campaign IO saved and generated successfully!" in io_form_page.get_success_message()
    io_form_page.select_from_modal(io_data['io_object']['campaign'], IoFormLocators.campaign_label)
    time.sleep(io_form_page.TWO_SEC_DELAY)
    io_form_page.set_text_using_tag_attribute(io_form_page.input_tag, io_form_page.class_attribute,
                                              IoFormLocators.form_control_media_budget_class, io_data['io_object'][
                                                  'media_budget'])
    io_form_page.click_on_element(IoFormLocators.save_and_generate_io_button_locator)
    assert "Campaign IO saved and generated successfully!" in io_form_page.get_success_message()

    # CREATING INVOICE ADDING PAYMENT
    io_form_page.click_on_specific_button(IoFormLocators.create_invoice_label)
    io_form_page.click_on_element(InvoiceFormLocators.save_and_generate_invoice_button_locator)
    io_form_page.click_on_specific_button(InvoiceFormLocators.add_payment_button)
    time.sleep(2)
    io_form_page.set_value_into_specific_input_field(InvoiceFormLocators.amount_paid_label, "1")
    io_form_page.click_on_specific_button(InvoiceFormLocators.save_button)
    driver.get(io_url)

    # GETTING OPEN IOS, CREDIT LIMIT LEVEL, FINANCE BALANCE & OPEN IOS AMOUNT
    bd_currency_rate = CurrencyUtils.pull_specific_currency_rate_data_db(13)
    open_ios, io_amounts = IoUtils.pull_open_ios_from_db()
    finance_balances = IoUtils.pull_finance_balances_from_db()
    open_io_string = ""
    if len(open_ios) > 0:
        for open_io in open_ios:
            open_io_string += (str(open_io).split("."))[0]
            if open_ios[len(open_ios) - 1] != open_io:
                open_io_string += ", "
    profile_finance_status_data['profile_finance_data']['open_ios'] = open_io_string

    io_amount_list = []
    if len(io_amounts) > 0:
        for io_amount in io_amounts:
            io_amount_string = (str(io_amount)).replace("[", "").replace('"', "").replace("]", "")
            io_amount_list.append(str(io_amount_string))
    open_io_amount = sum(map(float, io_amount_list))

    total_finance_balances = sum(map(float, finance_balances))
    credit_limit_level = open_io_amount + total_finance_balances
    profile_finance_status_data['profile_finance_data']['open_ios_amount'] = "$" + "{:,.2f}".format(open_io_amount)
    profile_finance_status_data['profile_finance_data']['finance_balance'] = "$" + "{:,.2f}".format(
        total_finance_balances)
    profile_finance_status_data['profile_finance_data']['credit_limit_level'] = "$" + "{:,.2f}".format(
        credit_limit_level)
    profile_finance_status_data['profile_finance_data']['currency_rate'] = \
        profile_finance_status_data['profile_finance_data']['currency_rate'] + "{:,.2f}".format(bd_currency_rate)

    # DATA VERIFICATION
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'credit_limit_level'] = float(io_form_page.get_specific_finance_profile_status(
        IoFormLocators.credit_limit_level_label))
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'overdue'] = io_form_page.get_specific_finance_profile_status(IoFormLocators.overdue_label)
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'finance_balance'] = float(
        io_form_page.get_specific_finance_profile_status(IoFormLocators.finance_balance_label))
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'open_ios_amount'] = io_form_page.get_specific_finance_profile_status(IoFormLocators.open_ios_amount_label)
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'open_ios'] = io_form_page.get_specific_finance_profile_status(IoFormLocators.open_ios_label)
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'last_invoice'] = io_form_page.get_specific_finance_profile_status(IoFormLocators.last_invoice_label)
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'last_payment'] = io_form_page.get_specific_finance_profile_status(IoFormLocators.last_payment_label)
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'discount'] = io_form_page.get_specific_finance_profile_status(IoFormLocators.discount_label)
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'rebate'] = io_form_page.get_specific_finance_profile_status(IoFormLocators.rebate_label)
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'bonus'] = io_form_page.get_specific_finance_profile_status(IoFormLocators.bonus_label)
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'tax'] = io_form_page.get_specific_finance_profile_status(IoFormLocators.tax_label)
    pulled_profile_finance_status_data_from_gui['profile_finance_data'][
        'currency_rate'] = io_form_page.get_specific_finance_profile_status(IoFormLocators.currency_rate_label)
    print(generic_modules.ordered(pulled_profile_finance_status_data_from_gui))
    print(generic_modules.ordered(profile_finance_status_data))
    assert generic_modules.ordered(pulled_profile_finance_status_data_from_gui) == generic_modules.ordered(
        profile_finance_status_data)

    pulled_io_data_gui = copy.deepcopy(io_data)
    pulled_io_data_gui['io_main_information']['io_title'] = io_form_page.get_value_from_specific_input_field(
        IoFormLocators.io_title_label)
    pulled_io_data_gui['client_profile']['client'] = io_form_page.get_text_using_tag_attribute(
        io_form_page.span_tag, io_form_page.id_attribute, IoFormLocators.select2_client_container_id)
    pulled_io_data_gui['client_profile']['email'] = io_form_page.get_value_from_specific_input_field(
        IoFormLocators.email_label)
    pulled_io_data_gui['client_profile']['contact'] = io_form_page.get_value_from_specific_input_field(
        IoFormLocators.contact_label)
    pulled_io_data_gui['client_profile']['responsible_adOps'] = io_form_page.get_text_using_tag_attribute(
        io_form_page.span_tag, io_form_page.id_attribute, IoFormLocators.select2_responsible_adops_container_id)
    print(generic_modules.ordered(pulled_io_data_gui))
    print(generic_modules.ordered(io_data))
    assert all_data_verification_message == CompareUtil.verify_data(pulled_io_data_gui, io_data)
    generic_modules.step_info(
        "[END - RTB-6611] Validate whether the user is able to generate IO just by filling up the mandatory fields \n"
        "[END - RTB-6609] Validate Profile finance status are available in the io form page")


def test_io_form_page_two(login_by_user_type):
    config, driver = login_by_user_type
    io_form_page = DspDashboardIoForm(driver)
    io_list_page = DspDashboardIoList(driver)
    sidebar_navigation = DashboardSidebarPage(driver)
    navbar = DashboardNavbar(driver)

    # PROVIDED IO DATA IN GUI
    with open('assets/io/io_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = io_data['io_main_information'][
                                                     'io_title'] + generic_modules.get_random_string(5)

    generic_modules.step_info(
        "[START - RTB-6649] Validate whether the Responsible AdOps, Client company, Company profile, Payment term "
        "(days) and Currency rate fields are readonly")
    navbar.login_as("AutomationAgencyUser")
    sidebar_navigation.navigate_to_io()
    io_list_page.navigate_to_add_io()
    io_form_page.provide_io_main_information(io_data)
    io_form_page.provide_io_client_profile_info(io_data)
    assert False is io_form_page.is_specific_field_enabled(IoFormLocators.responsible_adops_label)
    assert False is io_form_page.is_specific_field_enabled(IoFormLocators.client_company_label)
    assert False is io_form_page.is_specific_field_enabled(IoFormLocators.company_profile_label)
    assert False is io_form_page.is_specific_field_enabled(IoFormLocators.currency_rate_label, is_input_field=True)
    assert False is io_form_page.is_specific_field_enabled(IoFormLocators.payment_term_days_label, is_input_field=True)

    navbar.logout_as()
    io_form_page.provide_io_main_information(io_data)
    io_form_page.provide_io_client_profile_info(io_data)
    assert False is io_form_page.is_specific_field_enabled(IoFormLocators.responsible_adops_label)
    assert True is io_form_page.is_specific_field_enabled(IoFormLocators.client_company_label)
    assert True is io_form_page.is_specific_field_enabled(IoFormLocators.company_profile_label)
    assert False is io_form_page.is_specific_field_enabled(IoFormLocators.currency_rate_label, is_input_field=True)
    assert True is io_form_page.is_specific_field_enabled(IoFormLocators.payment_term_days_label, is_input_field=True)
    generic_modules.step_info(
        "[END - RTB-6649] Validate whether the Responsible AdOps, Client company, Company profile, Payment term "
        "(days) and Currency rate fields are readonly")

    generic_modules.step_info(
        "[START - RTB-6655] Validate whether some fields are being auto-filled based on the selection of the Client")
    pulled_io_data_gui = copy.deepcopy(io_data)
    pulled_io_data_gui['client_profile']['client'] = io_form_page.get_text_using_tag_attribute(
        io_form_page.span_tag, io_form_page.id_attribute, IoFormLocators.select2_client_container_id)
    pulled_io_data_gui['client_profile']['email'] = io_form_page.get_value_from_specific_input_field(
        IoFormLocators.email_label).lower()
    pulled_io_data_gui['client_profile']['contact'] = io_form_page.get_value_from_specific_input_field(
        IoFormLocators.contact_label)
    pulled_io_data_gui['client_profile']['responsible_adOps'] = io_form_page.get_text_using_tag_attribute(
        io_form_page.span_tag, io_form_page.id_attribute, IoFormLocators.select2_responsible_adops_container_id)
    pulled_io_data_gui['client_profile']['client_company'] = io_form_page.get_text_using_tag_attribute(
        io_form_page.span_tag, io_form_page.id_attribute, IoFormLocators.select2_company_id_container_id)
    pulled_io_data_gui['billing_entity']['company_profile'] = io_form_page.get_text_using_tag_attribute(
        io_form_page.span_tag, io_form_page.id_attribute, IoFormLocators.select2_company_profile_container_id)
    pulled_io_data_gui['billing_entity']['sales_manager'] = io_form_page.get_text_using_tag_attribute(
        io_form_page.span_tag, io_form_page.id_attribute, IoFormLocators.select2_sales_manager_container_id)
    pulled_io_data_gui['billing_information']['currency'] = io_form_page.get_text_using_tag_attribute(
        io_form_page.span_tag, io_form_page.id_attribute, IoFormLocators.select2_currency_container_id)
    currency_rate = io_form_page.get_value_from_specific_input_field(
        IoFormLocators.currency_rate_label)
    split_currency_rate = currency_rate.split(".")
    pulled_io_data_gui['billing_information']['currency_rate'] = split_currency_rate[0]
    print(generic_modules.ordered(pulled_io_data_gui))
    print(generic_modules.ordered(io_data))
    assert all_data_verification_message == CompareUtil.verify_data(pulled_io_data_gui, io_data)
    generic_modules.step_info(
        "[END - RTB-6655] Validate whether some fields are being auto-filled based on the selection of the Client")

    generic_modules.step_info(
        "[START - RTB-6656] Validate whether the FinAdmin users are able to add multiple client company under "
        "Client Company dropdown and some fields are being auto updated based on the company selection")
    generic_modules.step_info(
        "[START - RTB-6658] Validate whether the finAdmin type users are able to change Company Profile. "
        "And Currency is also changing based on the selection of company profile")
    ngn_currency_rate = CurrencyUtils.pull_specific_currency_rate_data_db(102)
    test_data = {'client_company': 'Webcoupers', 'company_profile': 'Eskimi NG-NG', 'currency': 'Nigeria Naira (NGN)',
                 'currency_rate': ngn_currency_rate}
    io_form_page.select_dropdown_value(IoFormLocators.client_company_label, test_data['client_company'])
    time.sleep(2)
    alert_text = io_form_page.get_alert_text()
    io_form_page.accept_alert()
    pulled_test_data = copy.deepcopy(test_data)
    pulled_test_data['client_company'] = io_form_page.get_text_using_tag_attribute(
        io_form_page.span_tag, io_form_page.id_attribute, IoFormLocators.select2_company_id_container_id)
    pulled_test_data['company_profile'] = io_form_page.get_text_using_tag_attribute(
        io_form_page.span_tag, io_form_page.id_attribute, IoFormLocators.select2_company_profile_container_id)
    pulled_test_data['currency'] = io_form_page.get_text_using_tag_attribute(
        io_form_page.span_tag, io_form_page.id_attribute, IoFormLocators.select2_currency_container_id)
    time.sleep(2)
    pulled_test_data['currency_rate'] = float(io_form_page.get_value_from_specific_input_field(
        IoFormLocators.currency_rate_label, inner_html=True))
    print(pulled_test_data)
    print(test_data)
    assert pulled_test_data == test_data
    generic_modules.step_info(
        "[END - RTB-6656] Validate whether the FinAdmin users are able to add multiple client company under "
        "Client Company dropdown and some fields are being auto updated based on the company selection")
    generic_modules.step_info(
        "[END - RTB-6658] Validate whether the finAdmin type users are able to change Company Profile. "
        "And Currency is also changing based on the selection of company profile")

    generic_modules.step_info(
        "[START - RTB-6657] Validate whether the FinAdmin users are getting proper warning message while trying "
        "to change the client company with different company profile and currency")
    assert "Company profile usual currency and selected currency doesn't match" == alert_text
    generic_modules.step_info(
        "[END - RTB-6657] Validate whether the FinAdmin users are getting proper warning message while trying "
        "to change the client company with different company profile and currency")


def test_io_form_page_three(login_by_user_type):
    config, driver = login_by_user_type
    io_form_page = DspDashboardIoForm(driver)
    navbar = DashboardNavbar(driver)

    # PROVIDED IO DATA IN GUI
    with open('assets/io/io_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = io_data['io_main_information'][
                                                     'io_title'] + generic_modules.get_random_string(5)

    generic_modules.step_info(
        "[START - RTB-6659] Validate whether the users are able to select multiple campaigns from the Campaign field")
    io_creation_url = config['credential']['url'] + config['io-creation-page']['io-creation-url']
    campaign_list = ['MassEditAndDuplicateAutomationBannerCampaign01 (111248)',
                     'MassEditAndDuplicateAutomationBannerCampaign02 (111250)']
    driver.get(io_creation_url)
    io_form_page.provide_io_main_information(io_data)
    io_form_page.provide_io_client_profile_info(io_data)
    io_form_page.select_multiple_item_from_modal(campaign_list, IoFormLocators.campaign_label)
    io_form_page.click_on_element(IoFormLocators.save_and_generate_io_button_locator)
    io_url = driver.current_url
    driver.get(io_url)
    campaigns_from_gui = io_form_page.get_selected_multiple_items_from_modal(IoFormLocators.campaign_label)
    assert campaigns_from_gui == campaign_list
    io_form_page.click_on_specific_button(IoFormLocators.delete_label)
    time.sleep(io_form_page.TWO_SEC_DELAY)
    alert = driver.switch_to.alert
    alert.accept()

    navbar.login_as("AutomationAgencyUser")
    driver.get(io_creation_url)
    io_form_page.provide_io_main_information(io_data)
    io_form_page.provide_io_client_profile_info(io_data)
    io_form_page.select_multiple_item_from_modal(campaign_list, IoFormLocators.campaign_label)
    io_form_page.click_on_element(IoFormLocators.save_and_generate_io_button_locator)
    io_url = driver.current_url
    driver.get(io_url)
    campaigns_from_gui_2 = io_form_page.get_selected_multiple_items_from_modal(IoFormLocators.campaign_label)
    assert campaigns_from_gui_2 == campaign_list
    navbar.logout_as()
    generic_modules.step_info(
        "[END - RTB-6659] Validate whether the users are able to select multiple campaigns from the Campaign field")

    generic_modules.step_info(
        "[START - RTB-6660] Validate whether the media budget table is populating with proper information")
    test_data = {'media_budget': '12.00', 'channel': 'DSP', 'country': 'Bangladesh', 'from_date': '', 'due_date': '',
                 'campaign_type': 'CPM', 'impressions': '111', 'media_rate': "{:.2f}".format((12 / 111) * 1000)}
    current_date = io_form_page.get_current_date_with_specific_format("%Y-%m-%d")
    future_date = io_form_page.get_specific_date_with_specific_format("%Y-%m-%d", days_to_add=6)
    test_data['from_date'] = current_date
    test_data['due_date'] = future_date
    io_form_page.click_on_element(IoFormLocators.media_budget_arrow_xpath.format("1"), locator_initialization=True)
    io_form_page.set_text_using_tag_attribute(io_form_page.input_tag, io_form_page.class_attribute,
                                              IoFormLocators.form_control_media_budget_class, test_data['media_budget'])
    time.sleep(io_form_page.TWO_SEC_DELAY)
    io_form_page.click_on_element(IoFormLocators.channel_dropdown_locator)
    io_form_page.set_value_into_element(IoFormLocators.channel_text_field_locator, test_data['channel'] + Keys.ENTER)
    io_form_page.select_dropdown_value(IoFormLocators.country_label, test_data['country'])
    io_form_page.click_on_element(IoFormLocators.period_field_locator)
    io_form_page.click_on_element(IoFormLocators.seven_days_option_locator)
    time.sleep(io_form_page.ONE_SEC_DELAY)
    io_form_page.select_dropdown_value(IoFormLocators.campaign_type_label, test_data['campaign_type'])
    io_form_page.set_value_into_specific_input_field(IoFormLocators.impressions_label, test_data['impressions'],
                                                     tab_out=True)
    test_data_from_gui = copy.deepcopy(test_data)
    test_data_from_gui['channel'] = io_form_page.get_text_from_specific_media_budget_table(
        IoFormLocators.tr_serial1_id, IoFormLocators.channel_class, 1)
    test_data_from_gui['country'] = io_form_page.get_text_from_specific_media_budget_table(
        IoFormLocators.tr_serial1_id, IoFormLocators.country_row_class, 1)
    test_data_from_gui['from_date'] = io_form_page.get_text_from_specific_media_budget_table(
        IoFormLocators.tr_serial1_id, IoFormLocators.date_from_row_class, 1)
    test_data_from_gui['due_date'] = io_form_page.get_text_from_specific_media_budget_table(
        IoFormLocators.tr_serial1_id, IoFormLocators.date_to_row_class, 1)
    test_data_from_gui['campaign_type'] = io_form_page.get_text_from_specific_media_budget_table(
        IoFormLocators.tr_serial1_id, IoFormLocators.campaign_type_class, 1)
    test_data_from_gui['impressions'] = io_form_page.get_text_from_specific_media_budget_table(
        IoFormLocators.tr_serial1_id, IoFormLocators.impressions_class, 1)
    test_data_from_gui['media_rate'] = io_form_page.get_text_from_specific_media_budget_table(
        IoFormLocators.tr_serial1_id, IoFormLocators.cpm_rate_class, 1)
    test_data_from_gui['media_budget'] = io_form_page.get_text_from_specific_media_budget_table(
        IoFormLocators.tr_serial1_id, IoFormLocators.total_currency_class, 1)
    assert test_data_from_gui == test_data

    io_form_page.click_on_element(IoFormLocators.save_and_generate_io_button_locator)
    driver.get(io_url)
    test_data_from_gui_1 = copy.deepcopy(test_data)
    test_data_from_gui_1['channel'] = io_form_page.get_text_from_specific_media_budget_table(
        IoFormLocators.tr_serial1_id, IoFormLocators.channel_class, 1)
    test_data_from_gui_1['country'] = io_form_page.get_text_from_specific_media_budget_table(
        IoFormLocators.tr_serial1_id, IoFormLocators.country_row_class, 1)
    test_data_from_gui_1['from_date'] = io_form_page.get_text_from_specific_media_budget_table(
        IoFormLocators.tr_serial1_id, IoFormLocators.date_from_row_class, 1)
    test_data_from_gui_1['due_date'] = io_form_page.get_text_from_specific_media_budget_table(
        IoFormLocators.tr_serial1_id, IoFormLocators.date_to_row_class, 1)
    test_data_from_gui_1['campaign_type'] = io_form_page.get_text_from_specific_media_budget_table(
        IoFormLocators.tr_serial1_id, IoFormLocators.campaign_type_class, 1)
    test_data_from_gui_1['impressions'] = io_form_page.get_text_from_specific_media_budget_table(
        IoFormLocators.tr_serial1_id, IoFormLocators.impressions_class, 1)
    test_data_from_gui_1['media_rate'] = io_form_page.get_text_from_specific_media_budget_table(
        IoFormLocators.tr_serial1_id, IoFormLocators.cpm_rate_class, 1)
    test_data_from_gui_1['media_budget'] = io_form_page.get_text_from_specific_media_budget_table(
        IoFormLocators.tr_serial1_id, IoFormLocators.total_currency_class, 1)
    assert test_data_from_gui_1 == test_data
    generic_modules.step_info(
        "[END - RTB-6660] Validate whether the media budget table is populating with proper information")

    generic_modules.step_info(
        "[START - RTB-6711] Validate whether the users are able to add multiple media budget")
    test_data_2 = {'media_budget': '100.00', 'channel': 'DSP display', 'country': 'Afghanistan',
                   'from_date': current_date, 'due_date': future_date, 'campaign_type': 'CPC', 'clicks': '111',
                   'media_rate': "{:.2f}".format((100 / 111))}
    io_form_page.click_on_element(IoFormLocators.media_budget_plus_button_locator)
    io_form_page.click_on_element(IoFormLocators.media_budget_arrow_xpath.format("2"), locator_initialization=True)
    io_form_page.set_text_using_tag_attribute(io_form_page.input_tag, io_form_page.class_attribute,
                                              IoFormLocators.form_control_media_budget_class,
                                              test_data_2['media_budget'],
                                              index=2)
    time.sleep(io_form_page.TWO_SEC_DELAY)
    io_form_page.click_on_element(IoFormLocators.channel_dropdown_locator)
    io_form_page.set_value_into_element(IoFormLocators.channel_text_field_locator, test_data_2['channel'] + Keys.ENTER)
    io_form_page.select_dropdown_value(IoFormLocators.country_label, test_data_2['country'], index=2)
    time.sleep(io_form_page.ONE_SEC_DELAY)
    io_form_page.select_dropdown_value(IoFormLocators.campaign_type_label, test_data_2['campaign_type'], index=2)
    io_form_page.set_value_into_specific_input_field(IoFormLocators.clicks_label, test_data_2['clicks'],
                                                     tab_out=True)
    test_data_from_gui_3 = copy.deepcopy(test_data_2)
    test_data_from_gui_3['channel'] = io_form_page.get_text_from_specific_media_budget_table(
        IoFormLocators.tr_serial2_id, IoFormLocators.channel_class, 1)
    test_data_from_gui_3['country'] = io_form_page.get_text_from_specific_media_budget_table(
        IoFormLocators.tr_serial2_id, IoFormLocators.country_row_class, 1)
    test_data_from_gui_3['from_date'] = current_date
    test_data_from_gui_3['due_date'] = future_date
    test_data_from_gui_3['campaign_type'] = io_form_page.get_text_from_specific_media_budget_table(
        IoFormLocators.tr_serial2_id, IoFormLocators.campaign_type_class, 1)
    test_data_from_gui_3['clicks'] = io_form_page.get_text_from_specific_media_budget_table(
        IoFormLocators.tr_serial2_id, IoFormLocators.impressions_class, 1)
    test_data_from_gui_3['media_rate'] = io_form_page.get_text_from_specific_media_budget_table(
        IoFormLocators.tr_serial2_id, IoFormLocators.cpm_rate_class, 1)
    test_data_from_gui_3['media_budget'] = io_form_page.get_text_from_specific_media_budget_table(
        IoFormLocators.tr_serial2_id, IoFormLocators.total_currency_class, 1)
    assert test_data_from_gui_3 == test_data_2

    io_form_page.click_on_element(IoFormLocators.save_and_generate_io_button_locator)
    io_url = driver.current_url
    driver.get(io_url)
    test_data_from_gui_4 = copy.deepcopy(test_data_2)
    test_data_from_gui_4['channel'] = io_form_page.get_text_from_specific_media_budget_table(
        IoFormLocators.tr_serial2_id, IoFormLocators.channel_class, 1)
    test_data_from_gui_4['country'] = io_form_page.get_text_from_specific_media_budget_table(
        IoFormLocators.tr_serial2_id, IoFormLocators.country_row_class, 1)
    test_data_from_gui_4['from_date'] = current_date
    test_data_from_gui_4['due_date'] = future_date
    test_data_from_gui_4['campaign_type'] = io_form_page.get_text_from_specific_media_budget_table(
        IoFormLocators.tr_serial2_id, IoFormLocators.campaign_type_class, 1)
    test_data_from_gui_4['clicks'] = io_form_page.get_text_from_specific_media_budget_table(
        IoFormLocators.tr_serial2_id, IoFormLocators.impressions_class, 1)
    test_data_from_gui_4['media_rate'] = io_form_page.get_text_from_specific_media_budget_table(
        IoFormLocators.tr_serial2_id, IoFormLocators.cpm_rate_class, 1)
    test_data_from_gui_4['media_budget'] = io_form_page.get_text_from_specific_media_budget_table(
        IoFormLocators.tr_serial2_id, IoFormLocators.total_currency_class, 1)
    assert test_data_from_gui_4 == test_data_2
    generic_modules.step_info(
        "[END - RTB-6711] Validate whether the users are able to add multiple media budget")

    generic_modules.step_info(
        "[START - RTB-6713] Validate whether the Total media budget amount is showing proper data based on the added media budget")
    assert "112.00" == io_form_page.get_text_using_tag_attribute(
        io_form_page.div_tag, io_form_page.class_attribute, IoFormLocators.first_total_media_budget_class)
    generic_modules.step_info(
        "[END - RTB-6713] Validate whether the Total media budget amount is showing proper data based on the added media budget")

    generic_modules.step_info(
        "[START - RTB-6712] Validate whether the users are able to remove media budget")
    io_form_page.click_on_element(IoFormLocators.media_budget_remove_button_xpath.format("2"),
                                  locator_initialization=True)
    assert False is io_form_page.is_element_present(IoFormLocators.second_media_budget_table_locator, time_out=1)
    io_form_page.click_on_element(IoFormLocators.save_and_generate_io_button_locator)
    driver.get(io_url)
    assert False is io_form_page.is_element_present(IoFormLocators.second_media_budget_table_locator, time_out=1)
    generic_modules.step_info(
        "[END - RTB-6712] Validate whether the users are able to remove media budget")


def test_io_form_page_four(login_by_user_type):
    config, driver = login_by_user_type
    io_form_page = DspDashboardIoForm(driver)
    user_form_page = DashboardUserFormPage(driver)
    navbar = DashboardNavbar(driver)
    sidebar_navigation = DashboardSidebarPage(driver)
    io_list_page = DspDashboardIoList(driver)

    # PROVIDED IO DATA IN GUI
    with open('assets/io/io_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = io_data['io_main_information'][
                                                     'io_title'] + generic_modules.get_random_string(5)
    generic_modules.step_info(
        "[START - RTB-6714] Validate whether the FinAdmin users are able to edit IO-campaign execution comment (internal)")

    automation_admin_user_settings_url = config['credential']['url'] + config['user-settings-pages'][
        'automation-admin-user']

    try:
        # CHANGING THE USER SETTINGS
        driver.get(automation_admin_user_settings_url)
        io_form_page.click_on_element(UserFormLocators.billing_settings_locator)
        time.sleep(2)
        io_form_page.click_on_element(UserFormLocators.finance_options_section_expand_icon_locator)
        user_form_page.check_uncheck_checkbox(UserFormLocators.billing_all_io_proforma_invoice_checkbox, False)
        user_form_page.check_uncheck_checkbox(UserFormLocators.billing_invoice_create_and_view_its_clients_checkbox,
                                              True)
        user_form_page.check_uncheck_checkbox(UserFormLocators.billing_io_view_its_clients_only_checkbox, True)
        user_form_page.check_uncheck_checkbox(UserFormLocators.add_execution_comment_to_io_invoice_proforma_checkbox,
                                              False)
        io_form_page.click_on_element(UserFormLocators.save_button_locator)

        # CHECKING IO EXECUTION COMMENT FIELD
        io_creation_url = config['credential']['url'] + config['io-creation-page']['io-creation-url']
        driver.get(io_creation_url)
        io_form_page.provide_io_main_information(io_data)
        io_form_page.provide_io_client_profile_info(io_data)
        io_form_page.provide_io_total_media_budget_info(io_data)
        io_form_page.click_on_element(IoFormLocators.save_and_generate_io_button_locator)
        io_url = driver.current_url
        driver.get(io_url)
        io_execution_comment = io_form_page.get_text_using_tag_attribute(
            io_form_page.span_tag, io_form_page.id_attribute,
            IoFormLocators.select2_io_execution_comment_id_container_id)
        assert io_execution_comment == io_data['total_media_budget']['io_execution_comment']
        generic_modules.step_info(
            "[END - RTB-6714] Validate whether the FinAdmin users are able to edit IO-campaign execution comment (internal)")
    finally:
        driver.get(automation_admin_user_settings_url)
        io_form_page.click_on_element(UserFormLocators.billing_settings_locator)
        time.sleep(2)
        io_form_page.click_on_element(UserFormLocators.finance_options_section_expand_icon_locator)
        user_form_page.check_uncheck_checkbox(UserFormLocators.billing_all_io_proforma_invoice_checkbox, True)
        io_form_page.click_on_element(UserFormLocators.save_button_locator)

    generic_modules.step_info(
        "[START - RTB-6716] Validate whether the Non FinAdmin users are not being able to edit IO-campaign execution comment (internal)")
    automation_agency_user_settings_url = config['credential']['url'] + config['user-settings-pages'][
        'automation-agency-user']

    try:
        # CHANGING THE USER SETTINGS
        driver.get(automation_agency_user_settings_url)
        io_form_page.click_on_element(UserFormLocators.billing_settings_locator)
        time.sleep(2)
        io_form_page.click_on_element(UserFormLocators.finance_options_section_expand_icon_locator)
        user_form_page.check_uncheck_checkbox(UserFormLocators.billing_all_io_proforma_invoice_checkbox, False)
        user_form_page.check_uncheck_checkbox(UserFormLocators.billing_clients_management_margins_checkbox, False)
        user_form_page.check_uncheck_checkbox(UserFormLocators.billing_invoice_create_and_view_its_clients_checkbox,
                                              False)
        user_form_page.check_uncheck_checkbox(UserFormLocators.billing_io_view_its_clients_only_checkbox, True)
        user_form_page.check_uncheck_checkbox(UserFormLocators.add_execution_comment_to_io_invoice_proforma_checkbox,
                                              False)
        io_form_page.click_on_element(UserFormLocators.save_button_locator)

        # CHECKING IO EXECUTION COMMENT FIELD
        navbar.login_as("AutomationAgencyUser")
        sidebar_navigation.navigate_to_io()
        time.sleep(io_list_page.FIVE_SEC_DELAY)
        io_list_page.wait_for_visibility_of_element(IoListLocators.first_grid_item_locator)
        io_list_page.search_and_action(io_data['io_main_information']['io_title'])
        time.sleep(io_list_page.TWO_SEC_DELAY)
        assert False is io_form_page.is_element_present(
            IoListLocators.io_number_link_xpath.format(io_data['io_main_information']['io_title']), 1,
            locator_initialization=True)
        io_list_page.click_on_element(
            IoListLocators.three_dot_of_io_xpath.format(io_data['io_main_information']['io_title']),
            locator_initialization=True)
        assert False is io_form_page.is_element_present(IoListLocators.edit_execution_comment_option_locator, 1)
        navbar.logout_as()
        generic_modules.step_info(
            "[END - RTB-6716] Validate whether the Non FinAdmin users are not being able to edit IO-campaign execution comment (internal)")
    finally:
        driver.get(automation_agency_user_settings_url)
        io_form_page.click_on_element(UserFormLocators.billing_settings_locator)
        time.sleep(2)
        io_form_page.click_on_element(UserFormLocators.finance_options_section_expand_icon_locator)
        user_form_page.check_uncheck_checkbox(UserFormLocators.billing_all_io_proforma_invoice_checkbox, True)
        io_form_page.click_on_element(UserFormLocators.save_button_locator)
