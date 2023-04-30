from selenium.webdriver.common.by import By


class BrandSafetyKeywordsLocators:
    # [Start] locators
    keywords_list_locator = (By.XPATH, "(//table[@id='items_table']//tbody//tr//td[2])")
    add_keywords_locator = (By.XPATH, "//a[@id='add_item']")
    keyword_provide_field_locator = (By.XPATH, "(//input[@type='text'])[2]")
    save_button_modal_locator = (By.XPATH, "//button[@data-bb-handler='confirm']")
    success_message_locator = (By.XPATH, "//div[@class='alert alert-success alert-dismissible fade show']")
    confirm_alert_locator = (By.XPATH, "//button[@data-bb-handler='confirm']")
    brand_safety_link_locator = (By.XPATH, "//h3//a[@href='/admin?function=brandsafety-manage' and normalize-space(text()='Brand safety')]")
    loader_locator = (By.XPATH, "//div[@id='general_loader']")
    # [End] locators

    # [Start] Attributes
    delete_icon_locator_xpath = "//td[normalize-space(text()='{}')]//..//i//.."
    # [End] Attributes