from selenium.webdriver.common.by import By


class CampaignApproveLocators:
    # [Start] locators
    campaign_status_label_locator = (By.XPATH, "//span[contains(@class, 'campaign-status')]")
    tech_fee_locator = (By.XPATH, "//input[@name='dev_cpm']")
    impression_performance_metric_locator = (By.XPATH, "//label[@href='#ac-metric-targeting']")
    impression_performance_metric_viewability_locator = (By.XPATH, "//input[@name='metric[viewability]']")
    impression_performance_metric_ctr = (By.XPATH, "//input[@name='metric[click_through_rate]']")
    impression_performance_metric_vcr = (By.XPATH, "//input[@name='metric[video_completion_rate]']")
    custom_impression_tracking_locator = (By.XPATH, "//label[@href='#ac-tracking']")
    add_more_custom_impression_tracking_locator = (
    By.XPATH, "//label[@href='#ac-tracking']/following-sibling::div//button")
    custom_impression_tracking_textarea_locator = (By.XPATH, "//textarea[@class='ace_text-input']")
    viewability_and_video_support_locator = (By.XPATH, "//label[@href='#ac-viewability']")
    video_player_requirement_locator = (By.XPATH, "//label[@href='#ac-video-player-requirements']")
    mraid_support_locator = (By.XPATH, "//label[@href='#ac-mraid']")
    anti_fraud_setting_locator = (By.XPATH, "//label[@href='#ac-antifraud-settings']")
    enhanced_min_reach_locator = (By.XPATH, "//input[@name='reach_min']")
    enhanced_max_reach_locator = (By.XPATH, "//input[@name='reach_max']")
    campaign_also_run_eskimi_text_locator = (By.XPATH, "//*[@id='eskimi-campaign-id']")
    approve_button_locator = (By.XPATH, "//input[@value='Approve' and @value='Approve']")
    button_alert_ok_locator = (By.XPATH, '//button[@data-bb-handler="ok"]')
    delete_button_locator = (By.XPATH, "//a[@id='js-delete' and normalize-space(text())='Delete']")
    button_group_locator = (By.XPATH, "//a[contains(text(),'Buttons')]")
    ignore_button_locator = (By.XPATH, "//button[contains(text(), 'Ignore')]")
    close_button_locator = (By.XPATH, "//button[@class = 'btn btn-success' and contains(text(), 'Close')]")
    cancel_button_locator = (By.XPATH, "//button[contains(text(), 'CANCEL')]")
    reject_button_locator = (By.XPATH, "//a[contains(text(), 'Reject')]")
    reject_reason_textarea_locator = (By.XPATH, "//textarea[@id='reject-reason']")
    reject_close_button_locator = (By.XPATH, "//button[contains(text(), 'Close')]")
    reject_submit_button_locator = (By.XPATH, "//button[contains(text(), 'Submit')]")
    remove_completely_button_locator = (By.XPATH, "//a[contains(text(), 'Remove completely')]")
    app_site_games_locator = (By.XPATH, "//option[normalize-space()='Games (16781271 apps/sites)']")
    app_site_photography_locator = (By.XPATH, "//option[normalize-space()='Photography (376174 apps/sites)']")
    app_site_include_locator = (By.XPATH, "//label[normalize-space()='Include']//input[@name='sites_categories_type']")
    brand_safety_include_locator = (By.XPATH, "//label[normalize-space()='Include']//input[@name='brand_safety_sets[filter]']")
    advertisement_category_default_selected_locator = (By.XPATH, "//select[@id='js-categories']//option[@value='IAB24'][normalize-space()='IAB24 Uncategorized']")
    approve_edit_button_locator = (By.XPATH, "//a[@class='no-decoration action-link']//i[@class='fas fa-pencil-alt']")
    approve_report_button_locator = (By.XPATH, "//span[@class='expended-actions-menu d-xl-inline-block']//a[@title='View report']")
    approve_preview_button_locator = (By.XPATH, "//a[@class='no-decoration action-link']//i[@class='fas fa-globe-asia']")
    approve_three_dot_locator = (By.XPATH, "//a[@id='campaing-menu-action']//i[@class='fas fa-ellipsis-v']")
    approve_three_dot_edit_locator = (By.XPATH, "//a[@title='Edit'][normalize-space()='']")
    approve_three_dot_targeting_optimisation_locator = (By.XPATH, "//a[@title='Targeting optimisation']")
    approve_three_dot_report_locator = (By.XPATH, "//a[normalize-space()='View report']")
    approve_three_dot_preview_locator = (By.XPATH, "//a[normalize-space()='Preview in browser']")
    approve_three_dot_duplicate_campaign_locator = (By.XPATH, "//a[@title='Duplicate campaign']")
    approve_three_dot_changelog_locator = (By.XPATH, "//a[@title='Changelog']")
    approve_three_dot_pixels_locator = (By.XPATH, "//a[@title='Tracking pixels']")
    approve_click_url_locator = (By.XPATH, "//a[normalize-space()='https://business.eskimi.com']")
    # [End] locators

    # [Start] label names
    insertion_order_label = "Insertion order (IO)"
    advertiser_name_label = "Advertiser name"
    advertiser_category_label = "Advertisement category"
    app_site_category_label = "App/Site category"
    brand_safety_label = "Brand safety"
    email_report_label = "Email reports"
    budget_pacing_label = "Budget pacing"
    daily_budget_recalculation_label = "Daily budget recalculation"
    email_report_frequency_label = "Report frequency"
    email_report_hour_label = "Report hour"
    email_report_day_label = "Report day"
    group_by_io_label = "Group by IO"
    email_attachments_label = "Email attachments"
    generate_insight_report_label = "Generate insights report"
    strict_size_placement_label = "Strict creative size placement"
    multiple_bid_per_second_label = "Allow multiple bids per user per second"
    campaign_also_run_on_eskimi_label = "Campaign also runs on Eskimi"
    margin_type_label = "Margin type"
    ad_exchange_margin_label = "Eskimi margin"
    # [End] label names

    # [Start] Attribute values
    custom_impression_tracking_dropdown_id = "ac-tracking"
    io_id = "select2-io-container"
    advertiser_name_id = "select2-adv-name-container"
    custom_impression_tracking_dropdown_xpath = "//div[@id='ac-tracking']/..//span[@class='select2-selection__rendered']"
    custom_impression_tracking_text_xpath = "//div[@id='ac-tracking']/..//span[@class='ace_text ace_xml']"
    viewability_and_video_support_div_id = "ac-viewability"
    video_player_requirement_div_id = "ac-video-player-requirements"
    mraid_support_div_id = "ac-mraid"
    anti_fraud_setting_div_id = "ac-antifraud-settings"
    ad_exchange_margin_text_xpath = "//label[normalize-space()='{}']/../following-sibling::div//input[@type='number']"
    # [End] Attribute values
