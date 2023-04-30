from selenium.webdriver.common.by import By


class UserFormLocators:
    # [Start] locators
    username_locator = (By.XPATH, "//input[@id='login']")
    password_locator = (By.XPATH, "//input[@id='password']")
    repeat_password_locator = (By.XPATH, "//input[@id='repeatPassword']")
    account_name_locator = (By.XPATH, "//input[@id='name']")
    email_locator = (By.XPATH, "//input[@name='main_info[email]']")
    contact_person_full_name_locator = (By.XPATH, "//input[@name='main_info[contact_person_full_name]']")
    contact_person_email_locator = (By.XPATH, "//input[@name='main_info[contact_person_email]']")
    contact_persona_phone_locator = (By.XPATH, "//input[@name='main_info[contact_person_phone]']")
    country_dropdown_locator = (By.XPATH, "//span[@id='select2-country-container']")
    company_dropdown_locator = (By.XPATH, "//span[@id='select2-company-container']")
    currency_dropdown_locator = (By.XPATH, "//span[@id='select2-currency-container']")
    currency_rate_locator = (By.XPATH, "//input[@id='currency_rate']")
    min_bid_locator = (By.XPATH, "//input[@id='min_bid']")
    max_bid_locator = (By.XPATH, "//input[@id='max_bid']")
    tech_fee_locator = (By.XPATH, "//input[@name='currency_setting[dev_cpm]']")
    save_button_locator = (By.XPATH, "//button[@type='submit']")
    cancel_button_locator = (By.XPATH, "//button[@type='reset']")
    billing_settings_locator = (By.XPATH, "//a[normalize-space()='Billing settings']")
    finance_options_section_expand_icon_locator = (
    By.XPATH, "//span[normalize-space()='Finance options']/following-sibling::span")
    # [End] locators

    # [Start] labels
    country_label = 'Country'
    company_label = 'Official company (organization) name'
    sales_manager_label = 'Sales manager'
    responsible_adops_label = 'Responsible adops'
    account_manager_label = 'Account manager'
    currency_label = 'Currency'
    billing_all_io_proforma_invoice_checkbox = "Billing: All (IO/PRO/Invoices)"
    billing_clients_management_margins_checkbox = "Billing: Clients management (margins)"
    billing_io_view_its_clients_only_checkbox = "Billing: IO (view it"
    billing_invoice_create_and_view_its_clients_checkbox = "Billing: Invoice (create and view it"
    add_execution_comment_to_io_invoice_proforma_checkbox = "Add execution comment to IO/Invoice/Proforma"
    # [End] labels
