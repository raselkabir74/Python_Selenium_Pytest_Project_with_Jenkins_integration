from pages.sidebar.sidebar import DashboardSidebarPage
from pages.traffic_discovery.traffic_discovery_list import DashboardTrafficDiscoveryPage


def test_traffic_discovery(login_by_user_type):
    config, driver = login_by_user_type
    side_bar_navigation = DashboardSidebarPage(driver)
    traffic_discovery_page = DashboardTrafficDiscoveryPage(driver)
    side_bar_navigation.navigate_to_traffic_discovery()
    assert traffic_discovery_page.is_traffic_discovery_table_existed()
    assert traffic_discovery_page.is_chart_graph_existed()
