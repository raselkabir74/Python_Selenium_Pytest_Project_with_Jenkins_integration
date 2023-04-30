from selenium.webdriver.common.by import By


class BrandSafetyFormLocators:
    # [Start] locators
    title_field_locator = (By.XPATH, "//input[@name='title']")
    keywords_upload_locator = (By.XPATH, "//input[@name='keywords']")
    default_dropdown_locator = (By.XPATH, "//span[@id='select2-brandsafety-set-is-default-container']")
    status_dropdown_locator = (By.XPATH, "//span[@id='select2-brandsafety-set-status-container']")
    save_button_locator = (By.XPATH, "//button[@type='submit']")
    cancel_link_locator = (By.XPATH, "//a[@class='btn btn-link btn-block']")
    # [End] locators

    # [Start] label names
    context_checkboxes_label = "Context options"
    find_url_label = "Find in URL"
    find_content_label = "Find in content"
    default_label = "Default"
    status_label = "Status"
    # [End] label names
