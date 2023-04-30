from selenium.webdriver.common.by import By


class TrafficDiscoveryLocators:
    # [Start] locators
    traffic_discovery_table_locator = (By.XPATH, "//div[@id='traffic_discovery_table_wrapper']")
    chart_line_graph_locator = (By.XPATH, "//div[@id='chart-line-graph']")
    # [End] locators