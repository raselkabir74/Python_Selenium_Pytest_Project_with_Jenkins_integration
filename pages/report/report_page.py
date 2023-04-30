from locators.report.report_page_locator import ReportPageLocators
from pages.base_page import BasePage


class DashboardReportage(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def generate_report(self):
        self.select_from_modal("VAST campaign test (ID: 72703)", ReportPageLocators.campaign_selection_label)
        self.select_dropdown_value(ReportPageLocators.report_view_mode_label, "Admin view")
        self.click_on_element(ReportPageLocators.date_range_link_locator)
        self.click_on_element(ReportPageLocators.all_date_locator)
        self.click_on_element(ReportPageLocators.update_report_button_locator)
        self.wait_for_element_to_be_invisible(ReportPageLocators.loader_icon_locator)

    def get_widget_list(self):
        widget_count = self.get_element_count(ReportPageLocators.widget_list_locator)
        widget_list = []
        for iteration in range(1, widget_count + 1):
            widget_list.append(
                self.get_attribute_value(ReportPageLocators.widget_list_xpath.format(iteration), "data-wf",
                                         locator_initialization=True))

        return widget_list

    def download_report(self, report_type='Excel'):
        self.click_on_element(ReportPageLocators.export_link_locator)
        if report_type == 'Excel':
            self.click_on_element(ReportPageLocators.excel_export_link_locator)
        elif report_type == 'PDF':
            self.click_on_element(ReportPageLocators.pdf_export_link_locator)
        elif report_type == 'PDF with chart':
            self.click_on_element(ReportPageLocators.pdf_chart_export_link_locator)
        success_message = self.get_element_text(ReportPageLocators.success_message_locator)
        self.wait_for_element_to_be_invisible(ReportPageLocators.success_message_locator)
        return success_message

