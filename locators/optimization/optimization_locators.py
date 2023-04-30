from selenium.webdriver.common.by import By


class OptimizationLocators:
    # [Start] Locators
    search_button_locator = (By.ID, "search-btn")
    app_site_column_locator = (By.XPATH, "//th[text()='App/site name']")
    grid_locator = (By.ID, "optimization_table")
    # [End] Locators

    # [Start] Label names
    campaign_label = "Campaign"
    optimise_by_label = "Optimise by"
    spent_label = "Spent"
    dates_label = "Dates"
    # [End] Label names

    # [Start] Dropdown items
    optimise_by_exchange_dropdown_item_value = "exchange"
    optimise_by_creative_dropdown_item_value = "creative"
    optimise_by_os_dropdown_item_value = "os"
    optimise_by_browser_dropdown_item_value = "browser"
    optimise_by_operator_dropdown_item_value = "operator"
    optimise_by_app_site_name_dropdown_item_value = "app_site_name"
    optimise_by_package_dropdown_item_value = "package"
    optimise_by_placement_dropdown_item_value = "placement"
    spent_based_on_cost_dropdown_item_value = "1"
    # [End] Dropdown items

    # [Start] Attribute values
    dropdown_optimize_by_css_selector = '[aria-labelledby="select2-optimise-by-container"] [role="presentation"]'
    dropdown_results_id = 'select2-optimise-by-results'
    table_optimization_id = 'optimization_table'
    # [End] Attribute values
