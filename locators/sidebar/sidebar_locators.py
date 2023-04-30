from selenium.webdriver.common.by import By


class SidebarLocators:
    #  [Start] label
    admin_menu_label = 'Admin tools'
    user_menu_label = 'Users'
    tool_menu_label = 'Tools'
    adops_tool_menu_label = 'AdOps tools'
    brand_safety_menu_label = 'Brand safety'
    package_menu_label = 'Packages'
    global_package_menu_label = 'Global packages'
    campaign_settings_label = 'Campaign settings'
    audiences_label = 'Audiences'
    global_audiences_label = 'Global audiences'
    client_companies_label = 'Clients companies'
    report_label = 'Reports'
    creative_sets_label = 'Creative sets'
    optimisation_label = 'Optimisation'
    traffic_discovery_label = 'Traffic discovery'
    billing_label = 'Billing'
    io_label = 'IO'
    invoice_label = 'Invoice'
    all_campaign_label = 'All campaigns'
    country_settings_label = 'Country settings'
    eskimi_billing_entities_label = 'Eskimi billing entities'
    # [End] label

    # [Start] Locators
    billing_menu_locator = (By.XPATH, "//span[text()='Billing']/../../../a")
    # [End] Locators
