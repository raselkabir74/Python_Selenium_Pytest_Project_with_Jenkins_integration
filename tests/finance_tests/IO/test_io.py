import json
import os
import time

import pytest

from configurations import generic_modules
from locators.io.credit_note_form_locator import CreditNoteFormLocators
from locators.io.invoice_form_locator import InvoiceFormLocators
from locators.io.invoice_list_locator import InvoiceListLocators
from locators.io.io_form_locator import IoFormLocators
from locators.io.io_list_locator import IoListLocators
from locators.io.proforma_form_locator import ProformaFormLocators
from locators.io.proforma_list_locator import ProformaListLocators
from locators.io.payments_log_locator import PaymentsLogLocators
from pages.io.invoice_form import DspDashboardInvoiceForm
from pages.io.invoice_list import DspDashboardInvoiceList
from pages.io.io_form import DspDashboardIoForm
from pages.io.io_list import DspDashboardIoList
from pages.io.payments_log import DspDashboardPaymentsLog
from pages.io.proforma_form import DspDashboardProformaForm
from pages.io.proforma_list import DspDashboardProformaList
from pages.io.credit_note_form import DspDashboardICreditNoteForm
from pages.sidebar.sidebar import DashboardSidebarPage
from utils.compare import CompareUtils as CompareUtil
global url
debug_mode = "JENKINS_URL" not in os.environ

@pytest.mark.dependency()
def test_add_edit_and_delete_io_and_invoice(login_by_user_type):
    config, driver = login_by_user_type
    io_form_page = DspDashboardIoForm(driver)
    io_list_page = DspDashboardIoList(driver)
    sidebar_navigation = DashboardSidebarPage(driver)

    # PROVIDED IO DATA IN GUI
    global url, debug_mode
    with open('assets/io/io_data.json') as json_file:
        io_data = json.load(json_file)
    io_data['io_main_information']['io_title'] = io_data['io_main_information'][
                                                     'io_title'] + generic_modules.get_random_string(5)
    with open('assets/temp/io_data.json', 'w') as json_file:
        json.dump(io_data, json_file)

    with open('assets/io/io_edit_data.json') as json_file:
        io_edit_data = json.load(json_file)
    io_edit_data['io_main_information']['io_title'] = io_edit_data['io_main_information'][
                                                          'io_title'] + generic_modules.get_random_string(5)
    with open('assets/temp/io_edit_data.json', 'w') as json_file:
        json.dump(io_edit_data, json_file)

    with open('assets/io/invoice_data.json') as json_file:
        invoice_data = json.load(json_file)
    invoice_data['invoice_main_information']['invoice_title'] = io_edit_data['io_main_information']['io_title']
    with open('assets/temp/invoice_data.json', 'w') as json_file:
        json.dump(invoice_data, json_file)

    with open('assets/io/invoice_edit_data.json') as json_file:
        invoice_edit_data = json.load(json_file)
    invoice_edit_data['invoice_main_information']['invoice_title'] = \
        invoice_edit_data['invoice_main_information']['invoice_title'] + generic_modules.get_random_string(5)
    with open('assets/temp/invoice_edit_data.json', 'w') as json_file:
        json.dump(invoice_edit_data, json_file)

    with open('assets/io/proforma_data.json') as json_file:
        proforma_data = json.load(json_file)
    proforma_data['proforma_main_information']['proforma_title'] = io_edit_data['io_main_information']['io_title']
    with open('assets/temp/proforma_data.json', 'w') as json_file:
        json.dump(proforma_data, json_file)

    with open('assets/io/proforma_edit_data.json') as json_file:
        proforma_edit_data = json.load(json_file)
    proforma_edit_data['proforma_main_information']['proforma_title'] = \
        proforma_edit_data['proforma_main_information']['proforma_title'] + generic_modules.get_random_string(5)
    with open('assets/temp/proforma_edit_data.json', 'w') as json_file:
        json.dump(proforma_edit_data, json_file)

    # IO CREATION
    sidebar_navigation.navigate_to_io()
    io_list_page.navigate_to_add_io()
    url = io_form_page.provide_io_data_and_save(io_data)
    assert "Campaign IO saved and generated successfully!" in io_form_page.get_success_message()

    # DATA VERIFICATION
    io_list_page.click_on_element(IoFormLocators.back_to_list_locator)
    io_list_page.select_dropdown_value(IoListLocators.client_company_label,
                                       IoListLocators.test_automation_company_data)
    time.sleep(io_list_page.FIVE_SEC_DELAY)
    io_list_page.wait_for_visibility_of_element(IoListLocators.first_grid_item_locator)
    io_list_page.search_and_action(io_data['io_main_information']['io_title'], "Edit IO")
    pulled_io_data_gui = io_form_page.get_io_information_from_gui(io_data)
    assert "All data verification is successful" == CompareUtil.verify_data(pulled_io_data_gui, io_data)

    # EDIT CREATED IO
    io_form_page.provide_io_data_and_save(io_edit_data, edit_io=True)
    assert "Campaign IO saved and generated successfully!" in io_form_page.get_success_message()

    # DATA VERIFICATION AFTER EDIT
    io_list_page.click_on_element(IoFormLocators.back_to_list_locator)
    io_list_page.select_dropdown_value(IoListLocators.client_company_label,
                                       IoListLocators.test_automation_company_data)
    io_list_page.wait_for_visibility_of_element(IoListLocators.first_grid_item_locator)
    io_list_page.search_and_action(io_edit_data['io_main_information']['io_title'], "Edit IO")
    pulled_io_data_gui_after_edit = io_form_page.get_io_information_from_gui(io_edit_data)
    assert "All data verification is successful" == CompareUtil.verify_data(pulled_io_data_gui_after_edit,
                                                                            io_edit_data)


@pytest.mark.dependency(depends=['test_add_edit_and_delete_io_and_invoice'])
def test_add_edit_and_delete_io_and_invoice_two(login_by_user_type):
    config, driver = login_by_user_type
    io_list_page = DspDashboardIoList(driver)
    invoice_form_page = DspDashboardInvoiceForm(driver)
    invoice_list_page = DspDashboardInvoiceList(driver)
    credit_note_page = DspDashboardICreditNoteForm(driver)
    sidebar_navigation = DashboardSidebarPage(driver)

    # PROVIDED IO DATA IN GUI
    global url, debug_mode
    with open('assets/temp/io_edit_data.json') as json_file:
        io_edit_data = json.load(json_file)

    with open('assets/temp/invoice_data.json') as json_file:
        invoice_data = json.load(json_file)

    with open('assets/temp/invoice_edit_data.json') as json_file:
        invoice_edit_data = json.load(json_file)

    with open('assets/io/payment_data.json') as json_file:
        payment_data = json.load(json_file)

    with open('assets/io/credit_note_data.json') as json_file:
        credit_note_data = json.load(json_file)

    with open('assets/io/payment_data_after_credit_note.json') as json_file:
        payment_data_after_credit_note = json.load(json_file)

    # INVOICE CREATION
    if debug_mode:
        sidebar_navigation.navigate_to_io()
        io_list_page.select_dropdown_value(IoListLocators.client_company_label,
                                           IoListLocators.test_automation_company_data)
        time.sleep(io_list_page.FIVE_SEC_DELAY)
        io_list_page.wait_for_visibility_of_element(IoListLocators.first_grid_item_locator)
        io_list_page.search_and_action(io_edit_data['io_main_information']['io_title'], "Invoice")
    else:
        io_list_page.driver.get(url)
        io_list_page.click_on_specific_button(IoFormLocators.create_invoice_label)
    io_list_page.click_on_element(InvoiceFormLocators.save_and_generate_invoice_button_locator)
    invoice_url = io_list_page.driver.current_url
    io_list_page.wait_for_visibility_of_element(InvoiceFormLocators.success_message_locator)
    assert "Invoice saved and generated successfully!" in invoice_form_page.get_success_message()

    # DATA VERIFICATION
    if debug_mode:
        invoice_list_page.click_on_element(InvoiceFormLocators.back_to_list_locator)
        io_list_page.select_dropdown_value(IoListLocators.client_company_label,
                                           IoListLocators.test_automation_company_data)
        invoice_list_page.wait_for_visibility_of_element(InvoiceListLocators.first_grid_item_locator)
        invoice_list_page.search_and_action(io_edit_data['io_main_information']['io_title'])
        time.sleep(io_list_page.FIVE_SEC_DELAY)
        invoice_list_page.click_on_specific_invoice(io_edit_data['io_main_information']['io_title'])
    else:
        invoice_list_page.driver.get(invoice_url)
    pulled_invoice_data_gui = invoice_form_page.get_invoice_information_from_gui(invoice_data)
    print(generic_modules.ordered(pulled_invoice_data_gui))
    print(generic_modules.ordered(invoice_data))
    assert "All data verification is successful" == CompareUtil.verify_data(pulled_invoice_data_gui,
                                                                            invoice_data)

    # EDIT CREATED INVOICE
    invoice_form_page.provide_invoice_data_and_save(invoice_edit_data, edit_invoice=True)
    assert "Invoice saved and generated successfully!" in invoice_form_page.get_success_message()

    # DATA VERIFICATION AFTER EDIT
    if debug_mode:
        invoice_list_page.click_on_element(InvoiceFormLocators.back_to_list_locator)
        io_list_page.select_dropdown_value(IoListLocators.client_company_label,
                                           IoListLocators.test_automation_company_data)
        invoice_list_page.wait_for_visibility_of_element(InvoiceListLocators.first_grid_item_locator)
        time.sleep(io_list_page.FIVE_SEC_DELAY)
        invoice_list_page.click_on_specific_invoice(invoice_edit_data['invoice_main_information']['invoice_title'])
    else:
        invoice_list_page.driver.get(invoice_url)
    pulled_invoice_data_gui_after_edit = invoice_form_page.get_invoice_information_from_gui(invoice_edit_data)
    print(generic_modules.ordered(pulled_invoice_data_gui_after_edit))
    print(generic_modules.ordered(invoice_edit_data))
    assert "All data verification is successful" == CompareUtil.verify_data(pulled_invoice_data_gui_after_edit,
                                                                            invoice_edit_data)

    # INVOICE PAYMENT
    assert invoice_form_page.calculate_and_verify_vat_discount_and_total_amount_from_ui(invoice_edit_data)
    invoice_form_page.add_payment_into_invoice(payment_data)
    assert "Invoice payment has been added!" in invoice_form_page.get_success_message()
    pulled_payment_data = invoice_form_page.get_payment_data(table_number="2", row_number="1")
    assert "All data verification is successful" == CompareUtil.verify_data(pulled_payment_data, payment_data)
    pulled_total_payment_data = invoice_form_page.get_payment_data(table_number="2", row_number="2")
    assert "All data verification is successful" == CompareUtil.verify_data(pulled_total_payment_data, payment_data)

    # CREDIT NOTE
    credit_invoice_number = credit_note_page.add_credit_note_into_invoice(credit_note_data)
    credit_invoice_url = io_list_page.driver.current_url
    assert "Credit note saved successfully!" in credit_note_page.get_success_message()

    # DATA VERIFICATION FOR CREDIT NOTE
    if debug_mode:
        credit_note_page.click_on_element(CreditNoteFormLocators.back_to_invoice_list_locator)
        io_list_page.select_dropdown_value(IoListLocators.client_company_label,
                                           IoListLocators.test_automation_company_data)
        invoice_list_page.wait_for_visibility_of_element(InvoiceListLocators.first_grid_item_locator)
        time.sleep(io_list_page.FIVE_SEC_DELAY)
        invoice_list_page.click_on_specific_credit_invoice(credit_invoice_number)
    else:
        invoice_list_page.driver.get(credit_invoice_url)
    pulled_credit_note_data = credit_note_page.get_credit_invoice_data()
    print(generic_modules.ordered(pulled_credit_note_data))
    print(generic_modules.ordered(credit_note_data))
    assert "All data verification is successful" == CompareUtil.verify_data(pulled_credit_note_data,
                                                                            credit_note_data)

    # DATA VERIFICATION FOR CREDIT NOTE FROM INVOICE FORM PAGE
    if debug_mode:
        credit_note_page.click_on_element(CreditNoteFormLocators.back_to_invoice_list_locator)
        io_list_page.select_dropdown_value(IoListLocators.client_company_label,
                                           IoListLocators.test_automation_company_data)
        invoice_list_page.wait_for_visibility_of_element(InvoiceListLocators.first_grid_item_locator)
        time.sleep(io_list_page.FIVE_SEC_DELAY)
        invoice_list_page.click_on_specific_invoice(invoice_edit_data['invoice_main_information']['invoice_title'])
    else:
        invoice_list_page.driver.get(invoice_url)
    pulled_payment_data_after_credit_note = invoice_form_page.get_payment_data_after_credit_note()
    print(generic_modules.ordered(pulled_payment_data_after_credit_note))
    print(generic_modules.ordered(payment_data_after_credit_note))
    assert "All data verification is successful" == CompareUtil.verify_data(payment_data_after_credit_note,
                                                                            pulled_payment_data_after_credit_note)


@pytest.mark.dependency(
    depends=['test_add_edit_and_delete_io_and_invoice', 'test_add_edit_and_delete_io_and_invoice_two'])
def test_add_edit_and_delete_io_and_invoice_three(login_by_user_type):
    config, driver = login_by_user_type
    io_list_page = DspDashboardIoList(driver)
    sidebar_navigation = DashboardSidebarPage(driver)
    invoice_form_page = DspDashboardInvoiceForm(driver)
    proforma_form_page = DspDashboardProformaForm(driver)
    proforma_list_page = DspDashboardProformaList(driver)

    # PROVIDED IO DATA IN GUI
    with open('assets/temp/io_edit_data.json') as json_file:
        io_edit_data = json.load(json_file)

    with open('assets/temp/proforma_data.json') as json_file:
        proforma_data = json.load(json_file)

    with open('assets/temp/proforma_edit_data.json') as json_file:
        proforma_edit_data = json.load(json_file)

    with open('assets/io/payment_data.json') as json_file:
        payment_data = json.load(json_file)

    # PROFORMA CREATION
    sidebar_navigation.navigate_to_io()
    io_list_page.select_dropdown_value(IoListLocators.client_company_label,
                                       IoListLocators.test_automation_company_data)
    time.sleep(io_list_page.FIVE_SEC_DELAY)
    io_list_page.wait_for_visibility_of_element(IoListLocators.first_grid_item_locator)
    io_list_page.search_and_action(io_edit_data['io_main_information']['io_title'], "Add proforma")
    io_list_page.click_on_element(ProformaFormLocators.confirmation_yes_button_locator)
    io_list_page.click_on_element(ProformaFormLocators.save_and_generate_proforma_button_locator)
    io_list_page.wait_for_visibility_of_element(ProformaFormLocators.success_message_locator)
    assert "Proforma saved and generated" in proforma_form_page.get_success_message()

    # DATA VERIFICATION
    proforma_list_page.click_on_element(ProformaFormLocators.back_to_list_locator)
    io_list_page.select_dropdown_value(IoListLocators.client_company_label,
                                       IoListLocators.test_automation_company_data)
    proforma_list_page.wait_for_visibility_of_element(ProformaListLocators.first_grid_item_locator)
    proforma_list_page.search_and_action(io_edit_data['io_main_information']['io_title'])
    time.sleep(io_list_page.FIVE_SEC_DELAY)
    proforma_list_page.click_on_specific_proforma(io_edit_data['io_main_information']['io_title'])
    pulled_proforma_data_gui = proforma_form_page.get_proforma_information_from_gui(proforma_data)
    print(generic_modules.ordered(pulled_proforma_data_gui))
    print(generic_modules.ordered(proforma_data))
    assert "All data verification is successful" == CompareUtil.verify_data(pulled_proforma_data_gui,
                                                                            proforma_data)

    # EDIT CREATED PROFORMA
    proforma_form_page.provide_proforma_data_and_save(proforma_edit_data, edit_proforma=True)
    assert "Proforma saved and generated" in proforma_form_page.get_success_message()

    # DATA VERIFICATION AFTER PROFORMA EDIT
    proforma_list_page.click_on_element(ProformaFormLocators.back_to_list_locator)
    io_list_page.select_dropdown_value(IoListLocators.client_company_label,
                                       IoListLocators.test_automation_company_data)
    proforma_list_page.wait_for_visibility_of_element(ProformaListLocators.first_grid_item_locator)
    proforma_list_page.search_and_action(io_edit_data['io_main_information']['io_title'])
    time.sleep(io_list_page.FIVE_SEC_DELAY)
    proforma_list_page.click_on_specific_proforma(io_edit_data['io_main_information']['io_title'])
    pulled_proforma_data_gui_after_edit = proforma_form_page.get_proforma_information_from_gui(proforma_edit_data)
    print(generic_modules.ordered(pulled_proforma_data_gui_after_edit))
    print(generic_modules.ordered(proforma_edit_data))
    assert "All data verification is successful" == CompareUtil.verify_data(pulled_proforma_data_gui_after_edit,
                                                                            proforma_edit_data)

    # PROFORMA PAYMENT
    invoice_form_page.add_payment_into_invoice(payment_data)
    time.sleep(3)
    status = proforma_form_page.get_element_text(ProformaFormLocators.status_locator)
    assert str(status).strip() == "Paid"


@pytest.mark.dependency(
    depends=['test_add_edit_and_delete_io_and_invoice', 'test_add_edit_and_delete_io_and_invoice_two',
             'test_add_edit_and_delete_io_and_invoice_three'])
def test_add_edit_and_delete_io_and_invoice_four(login_by_user_type):
    config, driver = login_by_user_type
    io_form_page = DspDashboardIoForm(driver)
    io_list_page = DspDashboardIoList(driver)
    sidebar_navigation = DashboardSidebarPage(driver)
    invoice_form_page = DspDashboardInvoiceForm(driver)
    invoice_list_page = DspDashboardInvoiceList(driver)
    payments_log_page = DspDashboardPaymentsLog(driver)

    with open('assets/temp/io_edit_data.json') as json_file:
        io_edit_data = json.load(json_file)

    with open('assets/temp/invoice_edit_data.json') as json_file:
        invoice_edit_data = json.load(json_file)

    folder_path = 'assets/temp'
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                os.rmdir(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))

    if "JENKINS_URL" not in os.environ:
        # PAYMENT DELETE
        sidebar_navigation.navigate_to_io()
        io_list_page.click_on_element(IoListLocators.logs_dropdown_icon_locator)
        io_list_page.click_on_element(IoListLocators.payment_actions_locator)
        if io_list_page.is_element_present(PaymentsLogLocators.delete_button_locator, 2):
            io_list_page.click_on_element(PaymentsLogLocators.delete_button_locator)
            io_list_page.click_on_element(PaymentsLogLocators.yes_button_locator)
            assert "payment has been deleted!" in payments_log_page.get_success_message()
        if io_list_page.is_element_present(PaymentsLogLocators.delete_button_locator, 2):
            io_list_page.click_on_element(PaymentsLogLocators.delete_button_locator)
            io_list_page.click_on_element(PaymentsLogLocators.yes_button_locator)
            assert "payment has been deleted!" in payments_log_page.get_success_message()
        if io_list_page.is_element_present(PaymentsLogLocators.delete_button_locator, 2):
            io_list_page.click_on_element(PaymentsLogLocators.delete_button_locator)
            io_list_page.click_on_element(PaymentsLogLocators.yes_button_locator)
            assert "payment has been deleted!" in payments_log_page.get_success_message()

        # INVOICE CLEAN UP
        sidebar_navigation.navigate_to_invoice()
        invoice_list_page.wait_for_visibility_of_element(InvoiceListLocators.first_grid_item_locator)
        time.sleep(2)
        invoice_list_page.click_on_specific_invoice(invoice_edit_data['invoice_main_information']['invoice_title'])
        io_list_page.click_on_specific_button(InvoiceFormLocators.delete_label)
        time.sleep(io_list_page.TWO_SEC_DELAY)
        alert = io_list_page.driver.switch_to.alert
        alert.accept()
        assert "Invoice has been deleted!" in invoice_form_page.get_success_message()

        # IO CLEAN UP
        sidebar_navigation.navigate_to_io()
        io_list_page.select_dropdown_value(IoListLocators.client_company_label,
                                           IoListLocators.test_automation_company_data)
        io_list_page.wait_for_visibility_of_element(IoListLocators.first_grid_item_locator)
        io_list_page.search_and_action(io_edit_data['io_main_information']['io_title'], "Edit IO")
        io_list_page.click_on_specific_button(IoFormLocators.delete_label)
        time.sleep(io_list_page.TWO_SEC_DELAY)
        alert = io_list_page.driver.switch_to.alert
        alert.accept()
        assert "IO has been deleted!" in io_form_page.get_success_message()
    else:
        pass
