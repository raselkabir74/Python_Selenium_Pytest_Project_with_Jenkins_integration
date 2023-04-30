from selenium.webdriver.common.by import By


class CompanyFormLocators:
    # [Start] locators
    company_name_locator = (By.XPATH, "//input[@name='title']")
    country_dropdown_locator = (By.XPATH, "//span[@id='select2-country-container']")
    company_address_textarea_locator = (By.XPATH, "//textarea[@name='address']")
    company_registration_number_locator = (By.XPATH, "//input[@name='code']")
    company_vat_id_locator = (By.XPATH, "//input[@name='vat_id']")
    company_financial_contact_name_locator = (By.XPATH, "//input[@name='financial_contact_name']")
    company_financial_contact_email_locator = (By.XPATH, "//input[@name='financial_contact_email']")
    company_financial_phone_number_locator = (By.XPATH, "//input[@name='finance_phone']")
    company_payment_term_locator = (By.XPATH, "//input[@name='payment_term']")
    company_discount_locator = (By.XPATH, "//input[@name='discount']")
    company_rebate_locator = (By.XPATH, "//input[@name='rebate']")
    company_bonus_locator = (By.XPATH, "//input[@name='bonus']")
    company_tax_locator = (By.XPATH, "//input[@name='tax']")
    collection_person_dropdown_locator = (By.XPATH, "//span[@id='select2-collection_person_id-container']")
    client_tier_dropdown_locator = (By.XPATH, "//span[@id='select2-tier-container']")
    save_button_locator = (By.XPATH, "//button[@type='submit']")
    cancel_button_locator = (By.XPATH, "//a[normalize-space()='CANCEL']")
    # [End] locators

    # [Start] labels
    country_label = 'Country'
    collection_person_label = 'Collection person'
    client_tier_label = 'Client Tier'
    # [End] labels