from locators.sidebar.sidebar_locators import SidebarLocators
from pages.base_page import BasePage


class DashboardSidebarPage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def navigate_to_admin_user_page(self):
        self.click_on_sidebar_menu(SidebarLocators.admin_menu_label)
        self.click_on_sidebar_menu(SidebarLocators.user_menu_label)

    def navigate_to_packages(self):
        self.click_on_sidebar_menu(SidebarLocators.tool_menu_label)
        self.click_on_sidebar_menu(SidebarLocators.package_menu_label)

    def navigate_to_campaign_settings(self):
        self.click_on_sidebar_menu(SidebarLocators.campaign_settings_label)

    def navigate_to_audiences(self):
        self.click_on_sidebar_menu(SidebarLocators.tool_menu_label)
        self.click_on_sidebar_menu(SidebarLocators.audiences_label)

    def navigate_to_reports(self):
        self.click_on_sidebar_menu(SidebarLocators.report_label)

    def navigate_to_creative_set(self):
        self.click_on_sidebar_menu(SidebarLocators.creative_sets_label)

    def navigate_to_optimisation(self):
        self.click_on_sidebar_menu(SidebarLocators.tool_menu_label)
        self.click_on_sidebar_menu(SidebarLocators.optimisation_label)

    def navigate_to_traffic_discovery(self):
        self.click_on_sidebar_menu(SidebarLocators.tool_menu_label)
        self.click_on_sidebar_menu(SidebarLocators.traffic_discovery_label)

    def navigate_to_global_packages(self):
        self.click_on_sidebar_menu(SidebarLocators.adops_tool_menu_label)
        self.click_on_sidebar_menu(SidebarLocators.global_package_menu_label)

    def navigate_to_global_audiences(self):
        self.click_on_sidebar_menu(SidebarLocators.adops_tool_menu_label)
        self.click_on_sidebar_menu(SidebarLocators.global_audiences_label)

    def navigate_to_io(self):
        is_expand = self.get_attribute_value(SidebarLocators.billing_menu_locator, "aria-expanded")
        if is_expand == 'false':
            self.click_on_sidebar_menu(SidebarLocators.billing_label)
        self.click_on_sidebar_menu(SidebarLocators.io_label)

    def navigate_to_invoice(self):
        is_expand = self.get_attribute_value(SidebarLocators.billing_menu_locator, "aria-expanded")
        if is_expand == 'false':
            self.click_on_sidebar_menu(SidebarLocators.billing_label)
        self.click_on_sidebar_menu(SidebarLocators.invoice_label)

    def navigate_to_client_companies(self):
        self.click_on_sidebar_menu(SidebarLocators.adops_tool_menu_label)
        self.click_on_sidebar_menu(SidebarLocators.client_companies_label)

    def navigate_to_brand_safety(self):
        self.click_on_sidebar_menu(SidebarLocators.tool_menu_label)
        self.click_on_sidebar_menu(SidebarLocators.brand_safety_menu_label)

    def navigate_to_all_campaigns(self):
        self.click_on_sidebar_menu(SidebarLocators.tool_menu_label)
        self.click_on_sidebar_menu(SidebarLocators.all_campaign_label)

    def navigate_to_country_settings(self):
        self.click_on_sidebar_menu(SidebarLocators.admin_menu_label)
        self.click_on_sidebar_menu(SidebarLocators.country_settings_label)

    def navigate_to_eskimi_billing_entities(self):
        self.click_on_sidebar_menu(SidebarLocators.admin_menu_label)
        self.click_on_sidebar_menu(SidebarLocators.eskimi_billing_entities_label)


