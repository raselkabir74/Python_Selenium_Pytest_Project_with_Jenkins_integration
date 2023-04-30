from selenium.webdriver.common.by import By


class BulkUserAddFormLocators:
    # [Start] locators
    email_input_locator = (By.XPATH,
                           "//label[normalize-space()='E-mail address(es)']/following-sibling::div/div[@class='bootstrap-tagsinput']/input")
    send_invitation_button_locator = (By.XPATH, "//button[normalize-space()='Send invitation' and @type='submit']")

    # [End] locators

    # [Start] labels
    agency_client_account_label = 'Agency/Client account'
    # [End] labels
