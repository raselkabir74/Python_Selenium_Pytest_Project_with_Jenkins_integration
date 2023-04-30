from locators.traffic_discovery.traffic_discovery_list_locators import TrafficDiscoveryLocators
from pages.base_page import BasePage


class DashboardTrafficDiscoveryPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def is_traffic_discovery_table_existed(self):
        return self.is_visible(TrafficDiscoveryLocators.traffic_discovery_table_locator)

    def is_chart_graph_existed(self):
        return self.is_visible(TrafficDiscoveryLocators.chart_line_graph_locator)
