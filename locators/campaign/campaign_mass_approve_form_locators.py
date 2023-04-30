from selenium.webdriver.common.by import By


class CampaignMassApproveFormLocators:
    # [Start] locators
    mass_approve_header_locator = (By.XPATH, "//a[@class='active' and normalize-space()='Mass approve']")
    approve_button_locator = (By.XPATH, "//button[@class='btn btn-success btn-block']")
    # [End] locators

    # [Start] Column names
    insertion_order_column = "Insertion"
    advertisement_category_column = "Advertisement category"
    app_site_category_column = "App/Site category"
    advertiser_name_column = "Advertiser name"
    budget_pacing_column = "Budget pacing"
    daily_budget_recalculation_column = "Daily budget recalculation"
    strict_creative_size_placement_column = "Strict creative size placement"
    multiple_bids_per_user_second_column = "Multiple bids/user/second"
    ad_exchange_column = "Ad exchanges"
    # [End] Column names

    # [Start] label name
    margin_type_label = "Margin type"
    ad_exchange_name_label = "Eskimi margin"
    # [End] label name

    # [Start] Attribute values
    campaign_mass_approve_form_id = "js-main-form"
    advertisement_category_modal_xpath = "//select[@name='campaigns[{}][excluded_cat][]']"
    app_site_category_modal_xpath = "//select[@name='campaigns[{}][sites_categories][]']"
    ad_exchange_text_field_xpath = "(//input[@data-name='{}'])[{}]/..//..//following-sibling::div//input"
    # [End] Attribute values
