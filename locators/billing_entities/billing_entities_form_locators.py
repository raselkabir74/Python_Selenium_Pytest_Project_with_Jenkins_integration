from selenium.webdriver.common.by import By


class BillingEntitiesFormLocators:
    # [Start] locators
    save_button_locator = (By.XPATH, "//button[@type='submit']")
    cancel_button_locator = (By.XPATH, "//a[text()='CANCEL']")
    country_value_locator = (By.XPATH, "//label[contains(text(), 'Country')]/..//span[@class='select2-selection__rendered']")
    # [End] locators

    # [Start] label names
    title_label = "Title"
    company_name_label = "Company name"
    address_label = "Address"
    postcode_label = "Postcode"
    country_label = "Country"
    phone_number_label = "Phone number"
    registration_number_label = "Registration number"
    vat_code_label = "VAT Code"
    bank_number_label = "Bank account number"
    # [End] label names

    # [Start] Attribute values

    # [End] Attribute values
