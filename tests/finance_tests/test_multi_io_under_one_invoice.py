import json
import os
import time

import pytest

from configurations import generic_modules, mysql
from locators.io.invoice_form_locator import InvoiceFormLocators
from locators.io.invoice_list_locator import InvoiceListLocators
from locators.io.io_form_locator import IoFormLocators
from locators.io.io_list_locator import IoListLocators
from locators.io.payments_log_locator import PaymentsLogLocators
from pages.io.invoice_form import DspDashboardInvoiceForm
from pages.io.invoice_list import DspDashboardInvoiceList
from pages.io.io_form import DspDashboardIoForm
from pages.io.io_list import DspDashboardIoList
from pages.sidebar.sidebar import DashboardSidebarPage
from utils.currency import CurrencyUtils
from utils.compare import CompareUtils as CompareUtil

global io_url_list, io_name_list, invoice_url_list


@pytest.mark.skipif("JENKINS_URL" in os.environ or mysql.mysql_connection_test(),
                    reason="Test need to be run manually and MySQL connection need to be established")
def test_multi_io_under_one_invoice(login_by_user_type):
    global io_url_list, io_name_list, invoice_url_list
    config, driver = login_by_user_type
    io_form_page = DspDashboardIoForm(driver)
    io_list_page = DspDashboardIoList(driver)
    invoice_form_page = DspDashboardInvoiceForm(driver)
    invoice_list_page = DspDashboardInvoiceList(driver)
    sidebar_navigation = DashboardSidebarPage(driver)

    try:
        # PROVIDED IO DATA IN GUI
        io_url_list = []
        invoice_url_list = []
        io_name_list = ["automation_ui_testing_" + generic_modules.get_random_string(5),
                        "automation_ui_testing_" + generic_modules.get_random_string(5),
                        "automation_ui_testing_" + generic_modules.get_random_string(5)]
        with open('assets/io/multi_io_data.json') as json_file:
            multi_io_data = json.load(json_file)
        with open('assets/io/invoice_data_for_multi_io.json') as json_file:
            invoice_data_for_multi_io = json.load(json_file)
        with open('assets/io/multi_io_invoice_payment_data.json') as json_file:
            multi_io_invoice_payment_data = json.load(json_file)
        currency_rates = CurrencyUtils.pull_currency_rate_data_db(
            multi_io_data['billing_information']['currency_ids'])

        # CALCULATIONS
        media_budgets = multi_io_data['io_object']['media_budget'].split(",")
        first_invoice_second_media_budget = (float(media_budgets[1]) / float(currency_rates[1])) / 2
        rounded_first_invoice_second_media_budget = round(first_invoice_second_media_budget, 2)
        base_amount = float(media_budgets[2]) + rounded_first_invoice_second_media_budget
        discount_amount = round(
            ((base_amount * float(invoice_data_for_multi_io['invoice_info']['discount'])) / 100), 2)
        vat_amount = round(
            (((base_amount - discount_amount) * float(invoice_data_for_multi_io['invoice_info']['vat'])) / 100), 2)
        total_amount = round((base_amount - discount_amount + vat_amount), 2)
        first_invoice_second_payment_amount = round((total_amount - first_invoice_second_media_budget), 2)

        # STORING CALCULATED VALUES
        invoice_data_for_multi_io['invoice_info']['media_budget_for_second_io'] = str(
            first_invoice_second_media_budget)
        multi_io_invoice_payment_data['payment_information']['amount_paid'] = str(
            first_invoice_second_media_budget)
        invoice_data_for_multi_io['invoice_info']['base_amount'] = "$" + "{:.2f}".format(base_amount)
        invoice_data_for_multi_io['invoice_info']['discount_in_payment'] = "$" + "{:.2f}".format(discount_amount)
        invoice_data_for_multi_io['invoice_info']['vat_in_payment'] = "$" + "{:.2f}".format(vat_amount)
        invoice_data_for_multi_io['invoice_info']['total_amount_in_payment'] = "$" + "{:.2f}".format(total_amount)

        # CREATING THREE IOs
        sidebar_navigation.navigate_to_io()

        # [START - RTB-6583] Validate Form navigation options are available and functional in the IO form page
        io_list_page.navigate_to_add_io()
        io_form_page.click_on_specific_form_nav_option(IoFormLocators.io_main_information_label)
        assert True is io_form_page.is_element_displayed(IoFormLocators.io_main_info_xpath)
        io_form_page.click_on_specific_form_nav_option(IoFormLocators.client_profile_label)
        assert True is io_form_page.is_element_displayed(IoFormLocators.client_profile_xpath)
        io_form_page.click_on_specific_form_nav_option(IoFormLocators.billing_entity_label)
        assert True is io_form_page.is_element_displayed(IoFormLocators.billing_entity_xpath)
        io_form_page.click_on_specific_form_nav_option(IoFormLocators.io_object_label)
        assert True is io_form_page.is_element_displayed(IoFormLocators.io_object_xpath)
        io_form_page.click_on_specific_form_nav_option(IoFormLocators.total_media_budget_label)
        assert True is io_form_page.is_element_displayed(IoFormLocators.total_media_budget_xpath)
        io_form_page.click_on_specific_form_nav_option(IoFormLocators.billing_information_label)
        assert True is io_form_page.is_element_displayed(IoFormLocators.billing_information_xpath)
        io_form_page.click_on_specific_form_nav_option(IoFormLocators.button_label)
        assert True is io_form_page.is_element_displayed(IoFormLocators.save_and_generate_io_xpath)
        io_form_page.click_on_specific_form_nav_option(IoFormLocators.io_main_information_label)
        # [END - RTB-6583] Validate Form navigation options are available and functional in the IO form page

        for io_name in io_name_list:
            multi_io_data['io_main_information']['io_title'] = io_name
            url = io_form_page.provide_multi_io_data_and_save(multi_io_data, index=io_name_list.index(io_name))
            io_url_list.append(url)
            io_list_page.click_on_element(IoFormLocators.back_to_list_locator, click_on_presence_of_element=True)
            io_list_page.navigate_to_add_io()

        print("INVOICE CREATION FOR THIRD AND SECOND IO")
        io_list_page.click_on_element(IoFormLocators.back_to_list_locator, click_on_presence_of_element=True)
        io_list_page.select_dropdown_value(IoListLocators.client_company_label,
                                           IoListLocators.test_automation_company_data)
        io_list_page.wait_for_visibility_of_element(IoListLocators.first_grid_item_locator)
        io_list_page.search_and_action(io_name_list[2], "Invoice")
        invoice_url = invoice_form_page.provide_invoice_data_for_multi_io_and_save(io_name_list[1],
                                                                                   invoice_data_for_multi_io)
        invoice_url_list.append(invoice_url)
        print("Assertion 1")
        assert "Invoice saved and generated successfully!" in invoice_form_page.get_success_message()

        print("DATA VERIFICATION AFTER CREATING FIRST INVOICE")
        io_list_page.driver.get(invoice_url_list[0])
        pulled_invoice_data_gui = invoice_form_page.get_invoice_information_from_gui_for_multi_io(
            invoice_data_for_multi_io)
        print(generic_modules.ordered(pulled_invoice_data_gui))
        print(generic_modules.ordered(invoice_data_for_multi_io))
        print("Assertion 2")
        assert "All data verification is successful" == CompareUtil.verify_data(pulled_invoice_data_gui,
                                                                                invoice_data_for_multi_io)

        print("FIRST INVOICE FIRST PAYMENT AND DATA VERIFICATION")
        invoice_form_page.add_payment_into_invoice(multi_io_invoice_payment_data)
        print("Assertion 3")
        assert False is invoice_form_page.is_element_present(InvoiceFormLocators.status_locator, 1)
        sidebar_navigation.navigate_to_io()
        io_list_page.select_dropdown_value(IoListLocators.client_company_label,
                                           IoListLocators.test_automation_company_data)
        io_list_page.wait_for_visibility_of_element(IoListLocators.first_grid_item_locator)
        io_list_page.driver.get(io_url_list[2])
        print("Assertion 4")
        assert False is invoice_form_page.is_element_present(IoFormLocators.status_locator, 1)
        io_list_page.click_on_element(IoFormLocators.back_to_list_locator, click_on_presence_of_element=True)
        io_list_page.wait_for_visibility_of_element(IoListLocators.first_grid_item_locator)
        io_list_page.driver.get(io_url_list[1])
        if io_list_page.is_alert_popup_available(2):
            io_list_page.accept_alert()
        print("Assertion 5")
        assert False is invoice_form_page.is_element_present(IoFormLocators.status_locator, 1)

        print("FIRST INVOICE SECOND PAYMENT AND DATA VERIFICATION")
        sidebar_navigation.navigate_to_invoice()
        multi_io_invoice_payment_data['payment_information']['amount_paid'] = str(
            first_invoice_second_payment_amount)
        io_list_page.driver.get(invoice_url_list[0])
        invoice_form_page.add_payment_into_invoice(multi_io_invoice_payment_data)
        print("Assertion 6")
        assert True is invoice_form_page.is_element_present(InvoiceFormLocators.status_locator)
        sidebar_navigation.navigate_to_io()
        io_list_page.select_dropdown_value(IoListLocators.client_company_label,
                                           IoListLocators.test_automation_company_data)
        io_list_page.wait_for_visibility_of_element(IoListLocators.first_grid_item_locator)
        io_list_page.driver.get(io_url_list[2])
        io_form_page.click_on_specific_form_nav_option(IoFormLocators.button_label)
        print("Assertion 7")
        assert True is invoice_form_page.is_element_present(IoFormLocators.status_locator)
        io_list_page.driver.get(io_url_list[1])
        if io_list_page.is_alert_popup_available(2):
            io_list_page.accept_alert()
        io_form_page.click_on_specific_form_nav_option(IoFormLocators.button_label)
        print("Assertion 8")
        assert False is invoice_form_page.is_element_present(IoFormLocators.status_locator, 1)

        # CALCULATIONS
        second_invoice_second_media_budget = ((float(media_budgets[1]) / float(currency_rates[1])) / 2) * float(
            currency_rates[0])
        rounded_second_invoice_second_media_budget = round(second_invoice_second_media_budget, 2)
        base_amount = float(media_budgets[0]) + rounded_second_invoice_second_media_budget
        discount_amount = round(
            ((base_amount * float(invoice_data_for_multi_io['invoice_info']['discount'])) / 100), 2)
        vat_amount = round(
            (((base_amount - discount_amount) * float(invoice_data_for_multi_io['invoice_info']['vat'])) / 100), 2)
        total_amount = round((base_amount - discount_amount + vat_amount), 2)
        second_invoice_second_payment_amount = round((total_amount - second_invoice_second_media_budget), 2)

        # STORING CALCULATED VALUES
        invoice_data_for_multi_io['invoice_info']['media_budget_for_second_io'] = str(
            second_invoice_second_media_budget)
        multi_io_invoice_payment_data['payment_information']['amount_paid'] = str(
            second_invoice_second_media_budget)
        invoice_data_for_multi_io['invoice_info']['base_amount'] = "BDT" + "{:.2f}".format(base_amount)
        invoice_data_for_multi_io['invoice_info']['discount_in_payment'] = "BDT" + "{:.2f}".format(discount_amount)
        invoice_data_for_multi_io['invoice_info']['vat_in_payment'] = "BDT" + "{:.2f}".format(vat_amount)
        invoice_data_for_multi_io['invoice_info']['total_amount_in_payment'] = "BDT" + "{:.2f}".format(total_amount)

        print("INVOICE CREATION FOR FIRST AND SECOND IO")
        io_list_page.click_on_element(IoFormLocators.back_to_list_locator, click_on_presence_of_element=True)
        io_list_page.select_dropdown_value(IoListLocators.client_company_label,
                                           IoListLocators.test_automation_company_data)
        io_list_page.wait_for_visibility_of_element(IoListLocators.first_grid_item_locator)
        io_list_page.search_and_action(io_name_list[0], "Invoice")
        if io_list_page.is_alert_popup_available(2):
            io_list_page.accept_alert()
        invoice_url = invoice_form_page.provide_invoice_data_for_multi_io_and_save(io_name_list[1], invoice_data_for_multi_io)
        invoice_url_list.append(invoice_url)
        if io_list_page.is_alert_popup_available(2):
            io_list_page.accept_alert()
        print("Assertion 9")
        assert "Invoice saved and generated successfully!" in invoice_form_page.get_success_message()

        print("DATA VERIFICATION AFTER CREATING SECOND INVOICE")
        io_list_page.driver.get(invoice_url_list[1])
        if io_list_page.is_alert_popup_available(2):
            io_list_page.accept_alert()
        pulled_invoice_data_gui_for_second_invoice = invoice_form_page.get_invoice_information_from_gui_for_multi_io(
            invoice_data_for_multi_io, second_invoice=True)
        print(generic_modules.ordered(pulled_invoice_data_gui_for_second_invoice))
        print(generic_modules.ordered(invoice_data_for_multi_io))
        print("Assertion 10")
        assert "All data verification is successful" == CompareUtil.verify_data(
            pulled_invoice_data_gui_for_second_invoice, invoice_data_for_multi_io)

        print("SECOND INVOICE FIRST PAYMENT AND DATA VERIFICATION")
        invoice_form_page.add_payment_into_invoice(multi_io_invoice_payment_data)
        if io_list_page.is_alert_popup_available(2):
            io_list_page.accept_alert()
        print("Assertion 11")
        assert False is invoice_form_page.is_element_present(InvoiceFormLocators.status_locator, 1)
        sidebar_navigation.navigate_to_io()
        io_list_page.driver.get(io_url_list[0])
        if io_list_page.is_alert_popup_available(2):
            io_list_page.accept_alert()
        io_form_page.click_on_specific_form_nav_option(IoFormLocators.button_label)
        print("Assertion 12")
        assert False is invoice_form_page.is_element_present(IoFormLocators.status_locator, 1)
        io_list_page.click_on_element(IoFormLocators.back_to_list_locator, click_on_presence_of_element=True)
        io_list_page.driver.get(io_url_list[1])
        if io_list_page.is_alert_popup_available(2):
            io_list_page.accept_alert()
        io_form_page.click_on_specific_form_nav_option(IoFormLocators.button_label)
        print("Assertion 13")
        assert True is invoice_form_page.is_element_present(IoFormLocators.status_locator)

        print("SECOND INVOICE SECOND PAYMENT AND DATA VERIFICATION")
        sidebar_navigation.navigate_to_invoice()
        multi_io_invoice_payment_data['payment_information']['amount_paid'] = str(
            second_invoice_second_payment_amount)
        io_list_page.driver.get(invoice_url_list[1])
        if io_list_page.is_alert_popup_available(2):
            io_list_page.accept_alert()
        invoice_form_page.add_payment_into_invoice(multi_io_invoice_payment_data)
        if io_list_page.is_alert_popup_available(2):
            io_list_page.accept_alert()
        print("Assertion 14")
        assert True is invoice_form_page.is_element_present(InvoiceFormLocators.status_locator)
        sidebar_navigation.navigate_to_io()
        io_list_page.select_dropdown_value(IoListLocators.client_company_label,
                                           IoListLocators.test_automation_company_data)
        io_list_page.driver.get(io_url_list[0])
        if io_list_page.is_alert_popup_available(2):
            io_list_page.accept_alert()
        io_form_page.click_on_specific_form_nav_option(IoFormLocators.button_label)
        print("Assertion 15")
        assert True is invoice_form_page.is_element_present(IoFormLocators.status_locator)
        io_list_page.click_on_element(IoFormLocators.back_to_list_locator, click_on_presence_of_element=True)
        io_list_page.driver.get(io_url_list[1])
        if io_list_page.is_alert_popup_available(2):
            io_list_page.accept_alert()
        io_form_page.click_on_specific_form_nav_option(IoFormLocators.button_label)
        print("Assertion 16")
        assert True is invoice_form_page.is_element_present(IoFormLocators.status_locator)
    except:
        assert False
    finally:
        # PAYMENT DELETE
        sidebar_navigation.navigate_to_io()
        io_list_page.click_on_element(IoListLocators.logs_dropdown_icon_locator)
        io_list_page.click_on_element(IoListLocators.payment_actions_locator)
        while io_list_page.is_element_present(PaymentsLogLocators.delete_button_locator, 5):
            io_list_page.click_on_element(PaymentsLogLocators.delete_button_locator)
            io_list_page.click_on_element(PaymentsLogLocators.yes_button_locator)

        # INVOICE CLEAN UP
        sidebar_navigation.navigate_to_invoice()
        io_list_page.select_dropdown_value(IoListLocators.client_company_label,
                                           IoListLocators.test_automation_company_data)
        invoice_list_page.wait_for_visibility_of_element(InvoiceListLocators.first_grid_item_locator)
        time.sleep(2)
        invoice_list_page.click_on_specific_invoice(io_name_list[0])
        if io_list_page.is_alert_popup_available(2):
            io_list_page.accept_alert()
        io_list_page.click_on_specific_button(InvoiceFormLocators.delete_label)
        time.sleep(io_list_page.ONE_SEC_DELAY)
        alert = io_list_page.driver.switch_to.alert
        alert.accept()

        sidebar_navigation.navigate_to_invoice()
        io_list_page.select_dropdown_value(IoListLocators.client_company_label,
                                           IoListLocators.test_automation_company_data)
        invoice_list_page.wait_for_visibility_of_element(InvoiceListLocators.first_grid_item_locator)
        time.sleep(2)
        invoice_list_page.click_on_specific_invoice(io_name_list[2])
        io_list_page.click_on_specific_button(InvoiceFormLocators.delete_label)
        time.sleep(io_list_page.ONE_SEC_DELAY)
        alert = io_list_page.driver.switch_to.alert
        alert.accept()

        for iteration in range(0, 3):
            if iteration == 0:
                index = 2
            elif iteration == 2:
                index = 0
            else:
                index = iteration
            io_list_page.driver.get(io_url_list[index])
            if iteration != 2:
                if io_list_page.is_alert_popup_available(2):
                    io_list_page.accept_alert()
            io_list_page.click_on_specific_button(IoFormLocators.delete_label)
            time.sleep(io_list_page.ONE_SEC_DELAY)
            alert = io_list_page.driver.switch_to.alert
            alert.accept()
