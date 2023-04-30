from selenium.webdriver.common.by import By


class CampaignSettingsLocator:
    #  [Start] locators
    campaign_search_field_locator = (By.ID, "filter_name")
    loader_locator = (By.XPATH, "//div[@id='loader-container']")
    search_box_locator = (By.XPATH, "//input[@id='filter_name']")
    campaign_name_edit_field_locator = (By.XPATH, "//input[@id='name']")
    bid_cpm_edit_field_locator = (By.XPATH, "//input[@id='bid_currency']")
    daily_budget_edit_field_locator = (By.XPATH, "//input[@id='budget_daily_currency']")
    total_budget_edit_field_locator = (By.XPATH, "//input[@id='budget_total_currency']")
    click_url_edit_field_locator = (By.XPATH, "//input[@id='click_url']")
    ad_domain_locator = (By.XPATH, "//span[@id='select2-ad_domain-container']")
    tick_or_cross_sign_click_url_locator = (By.XPATH, "//input[@id='click_url']//following-sibling::span//i[contains(@class, 'fa-check') or contains(@class ,'fa-times')]")
    ad_domain_search_field_locator = (By.XPATH, "//input[@class='select2-search__field']")
    remaining_text_locator = (By.XPATH, "//span[@id='remaining']")
    apply_to_all_creative_label_locator = (By.XPATH, "//label[@for='apply_to_all_creative']")
    campaign_search_button_locator = (By.XPATH, "//button[contains(text(),'Search')]")
    campaign_settings_locator = (By.XPATH, "//a[contains(text(),'Campaign settings')]")
    btn_create_locator = (By.XPATH, "//a[contains(@class, 'btn-create') and contains(@class ,'bg-blue')]")
    success_message_locator = (By.XPATH, "//div[@class='alert alert-success alert-dismissible fade show']")
    status_dropdown_locator = (By.XPATH, "//span[@id='select2-filter_status-container']")
    all_status_option_locator = (
        By.XPATH, "//ul[@id='select2-filter_status-results']/li[normalize-space(text())='All']")
    campaign_list_navigation = (By.XPATH, "//*[@class='back-to-list']//*[@class='fas fa-chevron-left']")
    campaign_settings_navigation = "(//dfn[@class='sidebar-tooltip']//*[contains(text(),'Campaign settings')])"
    campaign_stopped_status_locator = (By.XPATH, "//span[contains(text(), 'Sto.')]")
    # [End] locators

    # [Start] labels
    campaign_name_title = "Edit campaign name"
    bid_cpm_title = "Edit bid cpm"
    daily_budget_title = "Edit daily budget"
    total_budget_title = "Edit total budget"
    landing_page_title = "Edit landing page"
    creative_set_title = "Edit creative sets"
    creative_set_label = "Selected creative sets"
    # [End] labels

    # [Start] Attributes
    modal_save_button_xpath = "//div[@class='modal-footer']//button[@data-bb-handler='save' and @type='button' and contains(text(),'SAVE')]"
    status_dropdown_id = "select2-filter_status-container"
    campaign_name_xpath_locator = "(//a[contains(text(), '{}')])[{}]"
    # [End] Attributes
