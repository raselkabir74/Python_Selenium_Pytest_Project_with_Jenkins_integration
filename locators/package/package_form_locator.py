from selenium.webdriver.common.by import By


class PackageFormLocators:
    # [Start] labels
    package_name_label = "Package name"
    auction_type_label = "Auction type"
    csv_upload_label = "CSV upload"
    user_label = "Users"
    tag_label = "Tags"
    # [End] labels

    # [Start] locators
    save_button_locator = (By.XPATH, "//button[@type='submit' and contains(text(), 'Save')]")
    cancel_button_locator = (By.XPATH, "//button[@type='reset' and contains(text(), 'CANCEL')]")
    # [End] locators

    # [Start] Attribute values
    package_field_name = "name"
    user_field_class = "mselect-selection__rendered selected"
    selected_site_list_id = "js-selected-site-list"
    # [End] Attribute values
