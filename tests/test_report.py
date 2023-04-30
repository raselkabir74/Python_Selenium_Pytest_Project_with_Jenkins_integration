import os

import pytest

from pages.report.report_page import DashboardReportage
from pages.navbar.navbar import DashboardNavbar
from pages.sidebar.sidebar import DashboardSidebarPage
from utils.report import ReportUtils as ReportUtil
from utils.compare import CompareUtils as CompareUtil


def test_report(login_by_user_type):
    config, driver = login_by_user_type
    report_page = DashboardReportage(driver)
    navbar_page = DashboardNavbar(driver)
    sidebar_page = DashboardSidebarPage(driver)
    navbar_page.impersonate_user("Arunas B.")
    sidebar_page.navigate_to_reports()
    report_page.generate_report()
    pulled_widget_ids = report_page.get_widget_list()
    expected_widget_ids = ReportUtil.read_widget_ids()
    assert "All data verification is successful" == CompareUtil.verify_data(pulled_widget_ids, expected_widget_ids)
    assert "The report in Excel will be downloaded soon. You will receive the report in an email if you leave the page." in report_page.download_report(
        report_type='Excel')
    assert "The report in PDF will be downloaded soon. You will receive the report in an email if you leave the page." in report_page.download_report(
        report_type='PDF')
    assert "The report in PDF with charts will be downloaded soon. You will receive the report in an email if you leave the page." in report_page.download_report(
        report_type='PDF with chart')
