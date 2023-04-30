import json
import os
import time

import pytest

from configurations import mysql
from locators.campaign.campaign_approve_form_locator import CampaignApproveLocators
from locators.campaign.campaign_form_locator import CampaignFormLocators
from locators.campaign.campaign_list_locator import CampaignListLocators
from locators.report.report_page_locator import ReportPageLocators
from pages.campaign.campaign_approve_form import DspDashboardCampaignApprove
from pages.campaign.campaign_list import DspDashboardCampaignsList
from pages.campaign.campaign_settings_list import DspDashboardCampaignsSettings
from pages.campaign.campaign_view import DspDashboardCampaignView
from utils.campaigns import CampaignUtils as CampaignUtil


@pytest.mark.skipif("JENKINS_URL" in os.environ or mysql.mysql_connection_test(),
                    reason="Test need to be run manually and database connection need to be established")
def test_campaign_approve_all_options(login_by_user_type):
    config, driver = login_by_user_type
    campaign_list_page = DspDashboardCampaignsList(driver)
    campaign_approve_form = DspDashboardCampaignApprove(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_view = DspDashboardCampaignView(driver)
    with open('assets/campaign/campaign_approve_data.json') as json_file:
        provided_campaign_approve_data = json.load(json_file)
    # CREATE CAMPAIGN BY API
    campaign = CampaignUtil.create_campaign_by_api(config)
    campaign_settings_page.select_all_status()
    # APPROVE THE CAMPAIGN
    provided_campaign_approve_data = CampaignUtil.process_campaign_approve_data(provided_campaign_approve_data,
                                                                                single_approve=True)
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action(campaign['name'],'approve')
    campaign_approve_form.select_dropdown_value(CampaignApproveLocators.advertiser_name_label,
                                   dropdown_item=provided_campaign_approve_data['main_settings']['advertiser_name'])
    # CLICK ON EDIT ICON OPENS THE CAMPAIGN IN NEW TAB
    campaign_approve_form.click_on_element(CampaignApproveLocators.approve_edit_button_locator)
    campaign_approve_form.switch_to_new_window()
    assert campaign['name'] in campaign_approve_form.get_element_text(CampaignFormLocators.campaign_name_locator)
    campaign_approve_form.close_the_current_window_and_back_to_previous_window()
    # CLICK ON VIEW REPORT ICON OPENS REPORT
    campaign_approve_form.click_on_element(CampaignApproveLocators.approve_report_button_locator)
    campaign_approve_form.switch_to_new_window()
    assert 'Reports' in campaign_approve_form.get_element_text(ReportPageLocators.report_title_locator)
    campaign_approve_form.close_the_current_window_and_back_to_previous_window()
    # CLICK ON PREVIEW ICON
    campaign_approve_form.click_on_element(CampaignApproveLocators.approve_preview_button_locator)
    campaign_approve_form.switch_to_new_window()
    assert campaign['name'] in campaign_approve_form.get_element_text("//div[@id='container']/h3", locator_initialization=True)
    campaign_approve_form.close_the_current_window_and_back_to_previous_window()
    # CLICK ON THREE DOT-EDIT ACTIONS
    campaign_approve_form.click_on_element(CampaignApproveLocators.approve_three_dot_locator)
    time.sleep(2)
    campaign_approve_form.click_on_element(CampaignApproveLocators.approve_three_dot_edit_locator)
    campaign_approve_form.switch_to_new_window()
    assert campaign['name'] in campaign_approve_form.get_element_text(CampaignFormLocators.campaign_name_locator)
    campaign_approve_form.close_the_current_window_and_back_to_previous_window()
    # CLICK ON THREE DOT-TARGETING OPTIMISATION ACTIONS
    campaign_approve_form.click_on_element(CampaignApproveLocators.approve_three_dot_locator)
    time.sleep(2)
    campaign_approve_form.click_on_element(CampaignApproveLocators.approve_three_dot_targeting_optimisation_locator)
    campaign_approve_form.switch_to_new_window()
    assert 'Targeting optimisation' in campaign_approve_form.get_element_text("//div[@class='col-4 titles']/h4",locator_initialization=True)
    campaign_approve_form.close_the_current_window_and_back_to_previous_window()
    # CLICK ON THREE DOT-REPORT ACTIONS
    campaign_approve_form.click_on_element(CampaignApproveLocators.approve_three_dot_locator)
    time.sleep(2)
    campaign_approve_form.click_on_element(CampaignApproveLocators.approve_three_dot_report_locator)
    campaign_approve_form.switch_to_new_window()
    assert 'Reports' in campaign_approve_form.get_element_text(ReportPageLocators.report_title_locator)
    campaign_approve_form.close_the_current_window_and_back_to_previous_window()
    # CLICK ON THREE DOT-PREVIEW ACTIONS
    campaign_approve_form.click_on_element(CampaignApproveLocators.approve_three_dot_locator)
    time.sleep(2)
    campaign_approve_form.click_on_element(CampaignApproveLocators.approve_three_dot_preview_locator)
    campaign_approve_form.switch_to_new_window()
    assert campaign['name'] in campaign_approve_form.get_element_text("//div[@id='container']/h3", locator_initialization=True)
    campaign_approve_form.close_the_current_window_and_back_to_previous_window()
    # CLICK ON THREE DOT-DUPLICATE ACTIONS
    campaign_approve_form.click_on_element(CampaignApproveLocators.approve_three_dot_locator)
    time.sleep(2)
    campaign_approve_form.click_on_element(CampaignApproveLocators.approve_three_dot_duplicate_campaign_locator)
    campaign_approve_form.switch_to_new_window()
    assert 'Eskimi' in campaign_approve_form.get_attribute_value(CampaignFormLocators.platform_type_locator, "data-original-title")
    campaign_approve_form.close_the_current_window_and_back_to_previous_window()
    # CLICK ON THREE DOT-CHANGELOG ACTIONS
    campaign_approve_form.click_on_element(CampaignApproveLocators.approve_three_dot_locator)
    time.sleep(2)
    campaign_approve_form.click_on_element(CampaignApproveLocators.approve_three_dot_changelog_locator)
    campaign_approve_form.switch_to_new_window()
    assert 'Changelog' in campaign_approve_form.get_element_text("//div[@class='col-4 titles']/h3", locator_initialization=True)
    campaign_approve_form.close_the_current_window_and_back_to_previous_window()
    # CLICK ON THREE DOT-TRACKING PIXELS ACTIONS
    campaign_approve_form.click_on_element(CampaignApproveLocators.approve_three_dot_locator)
    time.sleep(2)
    campaign_approve_form.click_on_element(CampaignApproveLocators.approve_three_dot_pixels_locator)
    campaign_approve_form.switch_to_new_window()
    assert 'Tracking pixels' in campaign_approve_form.get_element_text("//div[@class='form-page']/h3", locator_initialization=True)
    campaign_approve_form.close_the_current_window_and_back_to_previous_window()
    # CLICK ON CLICK-URL
    campaign_approve_form.click_on_element(CampaignApproveLocators.approve_click_url_locator)
    campaign_approve_form.switch_to_new_window()
    assert "https://www.eskimi.com/" in driver.current_url
    campaign_approve_form.close_the_current_window_and_back_to_previous_window()
    campaign_approve_form.click_on_element(CampaignApproveLocators.app_site_include_locator)
    campaign_approve_form.click_on_element(CampaignApproveLocators.brand_safety_include_locator)
    campaign_approve_form.click_approve_button()
    campaign_approve_form.click_on_element(CampaignApproveLocators.close_button_locator)
    campaign_approve_form.click_on_element(CampaignApproveLocators.ignore_button_locator)
    # VERIFY THE DATA AND STATUS
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.search_and_action(campaign['name'],'approve')
    assert "Ready" in campaign_approve_form.get_campaign_status()
    assert "Eskimi" in campaign_approve_form.get_text_using_tag_attribute(campaign_approve_form.span_tag, campaign_approve_form.id_attribute, CampaignApproveLocators.advertiser_name_id)
    assert 'true' in campaign_approve_form.get_attribute_value(CampaignApproveLocators.app_site_games_locator,"selected")
    assert "true" in campaign_approve_form.get_attribute_value(CampaignApproveLocators.app_site_photography_locator,"selected")
    assert 'true' in campaign_approve_form.get_attribute_value(CampaignApproveLocators.app_site_include_locator, "checked")
    assert 'true' in campaign_approve_form.get_attribute_value(CampaignApproveLocators.brand_safety_include_locator, "checked")
    # REJECT CAMPAIGN
    campaign_approve_form.click_on_element(CampaignApproveLocators.reject_button_locator)
    campaign_approve_form.click_on_element(CampaignApproveLocators.reject_close_button_locator)
    campaign_approve_form.click_on_element(CampaignApproveLocators.reject_button_locator)
    campaign_approve_form.set_value_into_element(CampaignApproveLocators.reject_reason_textarea_locator, "Test")
    campaign_approve_form.click_on_element(CampaignApproveLocators.reject_submit_button_locator)
    # VERIFY THE DATA AND STATUS
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.search_and_action(campaign['name'], 'approve')
    assert "Rejected" in campaign_approve_form.get_campaign_status()
    # DELETE CAMPAIGN
    campaign_approve_form.click_delete_button()
    assert "Campaign deleted" in campaign_list_page.get_success_message()
    # REMOVE CAMPAIGN COMPLETELY
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.click_on_element(CampaignListLocators.status_dropdown_locator)
    campaign_list_page.click_on_element(CampaignListLocators.deleted_status_option_locator)
    campaign_list_page.search_and_action(campaign['name'], 'approve')
    assert "Deleted" in campaign_approve_form.get_campaign_status()
    # REMOVE COMPLETELY
    campaign_approve_form.click_on_element(CampaignApproveLocators.remove_completely_button_locator)
    campaign_approve_form.accept_alert()
    assert "Campaign deleted" in campaign_list_page.get_success_message()
