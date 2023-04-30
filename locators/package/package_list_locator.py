from selenium.webdriver.common.by import By


class PackageListLocators:
    # [Start] locators
    add_package_button_locator = (By.XPATH, "//a[@class='btn btn-primary bg-blue btn-create']")
    success_message_locator = (By.XPATH, "//div[@class='alert alert-success alert-dismissible fade show']")
    search_box_locator = (By.XPATH, "//input[@id='filter_name']")
    delete_link_locator = (By.XPATH, "//a[@data-role='delete']")
    edit_link_locator = (By.XPATH, "//a[@data-role='edit']")
    alert_confirm_button_locator = (By.XPATH, "//button[@data-bb-handler='confirm']")
    # [Start] locators

    # [Start] attribute values
    package_checkbox_xpath = "//table[@id='package_list_table']//a[@title='{}']/..//../td//input[@type='checkbox']"
    # [End] attribute values


