from selenium.webdriver.common.by import By


class BrandSafetyListLocators:
    # [Start] locators
    add_button_locator = (By.XPATH, "//a[@class='btn btn-primary bg-blue btn-create']")
    confirm_button_alert_locator = (By.XPATH, "//button[@data-bb-handler='confirm']")
    success_message_locator = (By.XPATH, "//div[@class='alert alert-success alert-dismissible fade show']")
    search_field_locator = (By.XPATH, "//input[@id='filter_name']")
    # [End] locators

    # [Start] attribute values
    brand_safety_option_edit_link_xpath = "//table[@id='brandsafety-sets-table']//a[normalize-space(text())='{}']"
    three_dot_of_campaign_xpath = "//a[contains(text(), '{}')]//..//..//..//i[@class='fas fa-ellipsis-v']"
    keyword_count_xpath = "//a[contains(text(), '{}')]//../following-sibling::td/following-sibling::td//a"
    # [End] attribute values

    # [Start] label names
    delete_label = "Delete"
    # [End] label names
