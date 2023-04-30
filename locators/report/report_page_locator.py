from selenium.webdriver.common.by import By


class ReportPageLocators:
    # [Start] locators
    report_title_locator = (By.XPATH, "//div[@class='col-12 col-md-4 titles']/h3")
    update_report_button_locator = (By.XPATH, "//div[@id='update-report-btn']//a")
    date_range_link_locator = (By.XPATH, "//div[@id='date-range']//input")
    all_date_locator = (By.XPATH, "//a[@data-key='all_time']")
    loader_icon_locator = (By.XPATH, "//a[@href='#tab-0']//i[@class='loader-icon']")
    widget_list_locator = (By.XPATH, "//*[@id='tab-0']//div[@class='widgets w-row']/div")
    success_message_locator = (By.XPATH, "//div[@class='alert alert-info alert-dismissible fade show']")
    export_link_locator = (By.XPATH, "//span[normalize-space(text())='Export']")
    excel_export_link_locator = (By.XPATH, "//span[normalize-space(text())='Excel']")
    pdf_export_link_locator = (By.XPATH, "//span[normalize-space(text())='PDF']")
    pdf_chart_export_link_locator = (By.XPATH, "//span[normalize-space(text())='PDF with charts']")
    # [Start] locators

    # [Start] label names
    report_view_mode_label = "View"
    campaign_selection_label = "Campaign"
    # [End] label names

    # [Start] Attributes
    widget_list_xpath = "//*[@id='tab-0']//div[@class='widgets w-row']/div[{}]"
    # [End] Attributes


