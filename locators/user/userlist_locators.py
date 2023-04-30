from selenium.webdriver.common.by import By


class UserListLocators:
    # [Start] locators
    add_user_button_locator = (By.XPATH, "//a[normalize-space()='Add user']")
    bulk_user_button_locator = (By.XPATH, "//a[normalize-space()='Add bulk user']")
    success_message_locator = (By.XPATH, "//div[@class='alert alert-success alert-dismissible fade show']")
    search_box_locator = (By.XPATH, "//input[@id='filter_name']")
    processing_loader_locator = (By.XPATH, "//div[@id='users-table_processing']")
    three_dot_locator = (By.XPATH, "//table[@id='users-table']//tr[@data-row-id='0']//td[@class='dropdown actions']//a")
    delete_option_locator = (By.XPATH, "//a[@title='Delete']")
    edit_option_locator = (By.XPATH, "//a[@title='Edit']")
    alert_confirm_button_locator = (By.XPATH, "//button[@data-bb-handler='confirm' and @type ='button']")
    # [End] locators
