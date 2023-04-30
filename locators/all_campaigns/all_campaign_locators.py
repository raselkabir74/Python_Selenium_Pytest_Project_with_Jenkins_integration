from selenium.webdriver.common.by import By


class AllCampaignFormLocators:
    # [Start] locators
    processing_locator = (By.XPATH, "//div[@id='accampaign_table_processing']")
    clear_all_locator = (By.XPATH, "//a[normalize-space(text()) = 'Clear All']")
    search_filter_locator = (By.XPATH, "//input[@id='filter_name']")
    three_dot_locator = (By.XPATH, "//table[@id='accampaign_table']//tr[@data-row-id='0']//td[@class='dropdown actions']//i")
    targeting_optimization_locator = (By.XPATH, "//a[@title='Targeting optimisation']")
    view_report_locator = (By.XPATH, "//a[@title='View report']")
    campaign_goals_locator = (By.XPATH, "//a[@title='Campaign goals']")
    confirm_campaign_locator = (By.XPATH, "//a[@title='Confirm campaign']")
    reject_campaign_locator = (By.XPATH, "//a[@title='Reject campaign']")
    delete_campaign_locator = (By.XPATH, "//a[@title='Delete campaign']")
    remove_completely_campaign_locator = (By.XPATH, "//a[@title='Remove completely']")
    # [End] locators

    # [Start] Attribute values
    table_row_status_xpath = "//td//span[@title='{}']"
    table_row_type_xpath = "//td//i[@title='{}']"
    table_row_country_xpath = "//span[@title='{}']"
    table_row_login_as_xpath = "//a[@title='Login as {}']"
    table_row_campaign_name_xpath = "//td//a[@title='{}']"
    table_row_last_approved_by_xpath = "//td[normalize-space(text())='{}']"
    status_filter_xpath = "//div[@id='page_filter']/..//select[@id='filter_status']"
    user_filter_xpath = "//div[@id='page_filter']/..//select[@id='filter_user']"
    country_filter_xpath = "//div[@id='page_filter']/..//select[@id='filter_country']"
    type_filter_xpath = "//div[@id='page_filter']/..//select[@id='filter_type']"
    last_approved_filter_xpath = "//div[@id='page_filter']/..//select[@id='filter_last_approved']"
    # [End] Attribute values









