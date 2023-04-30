from selenium.webdriver.common.by import Byclass InvoiceFormLocators:    # [Start] locators    save_and_generate_invoice_button_locator = (By.XPATH, "//input[@value='Save and generate invoice']")    success_message_locator = (By.XPATH, "//div[@class='alert alert-success alert-dismissible fade show']")    back_to_list_locator = (By.XPATH, "//a[normalize-space()='BACK TO LIST']")    invoice_object_dropdown_selected_item_locator = (By.XPATH, "//span[contains(@id, 'select2-invoice_object')]")    payment_details_section_locator = (        By.XPATH, "//span[normalize-space()='Payment details' and @class='tab2-selection__rendered']")    discount_field_locator = (By.XPATH, "//input[@name='discount']")    balance_field_locator = (By.XPATH, "//div[@id='form-step-box-i-6']//tbody[2]//tr[4]//td[2]")    balance_field_2_locator = (By.XPATH, "//div[@id='form-step-box-i-6']//tbody[2]//tr[5]//td[2]")    status_locator = (By.XPATH, "//p[@class='form-status-paid']")    first_grid_item_locator = (By.XPATH, "//table[@id='campaigns-invoice-table']//tbody//tr//a")    totals_and_payments_group_locator = (By.XPATH, "//a[normalize-space()='Totals & payments']")    billing_information_group_locator = (By.XPATH, "//a[normalize-space()='Billing information']")    buttons_group_locator = (By.XPATH, "//a[normalize-space()='Buttons']")    channel_dropdown_locator = (    By.XPATH, "//label[normalize-space()='Channel / Service']/..//span[@class='select2-selection__rendered']")    channel_text_field_locator = (By.XPATH, "//input[@class='select2-search__field']")    # [End] locators    # [Start] label names    invoice_title_label = "Invoice title"    campaign_label = "Campaign"    client_label = "Client"    sales_manager_label = "Sales manager"    channel_service_label = "Channel / Service"    notes_label = "Notes (PDF)"    currency_label = "Currency"    vat_label = "VAT"    delete_label = "Delete"    archive_label = "Archive"    email_label = "Email"    contact_label = "Contact"    use_notice_text_on_invoice_label = "Use notice text on invoice"    currency_rate_label = "Currency rate"    payment_term_days_label = "Payment term (days)"    invoice_object_label = "Invoice object"    amount_paid_label = "Amount paid"    bank_charges_label = "Bank Charges"    taxes_label = "Taxes"    rebate_label = "Rebate"    paid_amount_label = "Paid amount"    tax_label = "Tax"    discount_label = "Discount"    vat_2_label = "Vat"    base_amount_label = "Base amount"    total_amount_label = "Total amount"    bank_charges_2_label = "Bank charges"    total_label = "Total"    credit_label = "Credit"    select_io_label = "Select IO"    io_execution_comment_label = "IO-campaign execution comment (internal)"    # [End] label names    # [Start] Button names    credit_note_button = "Add credit note"    add_payment_button = "Add payment"    save_button = "Save"    # [End] Button names    # [Start] Attribute values    select2_client_container_id = "select2-client-container"    select2_company_profile_container_id = "select2-company_profile-container"    select2_sales_manager_container_id = "select2-sales_manager-container"    form_control_media_budget_class = "form-control media-budget"    first_total_media_budget_class = "span8 first total-media-budget"    select2_currency_container_id = "select2-currency-container"    select2_io_execution_comment_id_container_id = "select2-io_execution_comment_id-container"    discount_name = "discount"    form_step_box_i_6_div_id = "form-step-box-i-6"    paid_vat_id = "paid-vat"    paid_charges_id = "paid-charges"    paid_taxes_id = "paid-taxes"    paid_rebate_id = "paid-rebate"    media_budget_actual_amount_locator = \        "(//label[contains(., 'Media budget')]/..//span[@class='media-budget-io-amount'])[{}]"    media_budget_field_locator = \        "(//label[@class='media-budget-label']/..//input[contains(@name, 'invoice_media_budgets')])[{}]"    # [End] Attribute values