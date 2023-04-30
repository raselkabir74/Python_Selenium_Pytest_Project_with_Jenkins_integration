from selenium.webdriver.common.by import By


class CompanyListLocators:
    # [Start] locators
    add_company_button_locator = (By.XPATH, "//a[normalize-space()='Add new company']")
    success_message_locator = (By.XPATH, "//div[@class='alert alert-success alert-dismissible fade show']")
    search_box_locator = (By.XPATH, "//input[@id='filter_name']")
    delete_option_locator = (By.XPATH, "//a[@title='Delete']")
    edit_option_locator = (By.XPATH, "//a[@title='Edit']")
    alert_confirm_button_locator = (By.XPATH, "//button[@data-bb-handler='confirm' and @type ='button']")
    no_record_message_locator = (By.XPATH, "//td[@class='dataTables_empty']")
    # [End] locators

    # [Start] attributes
    three_dot_locator_xpath = "//table[@id='companies-table']//span[normalize-space()='{}']//..//..//..//td[@class='dropdown actions']"
    # [End] attributes
