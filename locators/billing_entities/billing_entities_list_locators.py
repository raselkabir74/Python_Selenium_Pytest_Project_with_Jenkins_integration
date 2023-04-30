from selenium.webdriver.common.by import By


class BillingEntitiesListLocators:
    # [Start] locators
    btn_create_locator = (By.XPATH, "//a[contains(@class, 'btn-create') and contains(@class ,'bg-blue')]")
    success_message_locator = (By.XPATH, "//div[@class='alert alert-success alert-dismissible fade show']")
    search_box_locator = (By.XPATH, "//input[@id='filter_name']")
    alert_confirm_button_locator = (By.XPATH, "//button[@data-bb-handler='confirm']")
    empty_row_locator = (By.XPATH, "//td[@class='dataTables_empty']")
    # [End] locators

    # [Start] Attributes
    three_dot_xpath = "//td[text()='{}']/..//a[@role='button']//i"
    edit_xpath = "//td[text()='{}']/..//a[@role='button']//..//a[@title='Edit']"
    delete_xpath = "//td[text()='{}']/..//a[@role='button']//..//a[@title='Delete']"
    # [End] Attributes
