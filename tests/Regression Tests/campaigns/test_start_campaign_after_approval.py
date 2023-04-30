import json
import os
import time

import pytest

from configurations import generic_modules, mysql
from locators.campaign.campaign_approve_form_locator import CampaignApproveLocators
from pages.base_page import BasePage
from pages.campaign.campaign_approve_form import DspDashboardCampaignApprove
from pages.campaign.campaign_form import DspDashboardCampaignsForm
from pages.campaign.campaign_settings_list import DspDashboardCampaignsSettings
from pages.campaign.campaign_view import DspDashboardCampaignView


@pytest.mark.skipif("JENKINS_URL" in os.environ or mysql.mysql_connection_test(),
                    reason="Test need to be run manually and database connection need to be established")
def test_start_campaign_after_approval_unchecked(login_by_user_type):
    config, driver = login_by_user_type
    base_page = BasePage(driver)
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_view = DspDashboardCampaignView(driver)
    campaign_approve = DspDashboardCampaignApprove(driver)

    with open('assets/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['name_and_type']['campaign_name'] = campaign_data['name_and_type'][
                                                          'campaign_name'] + generic_modules.get_random_string(5)
    # CREATE A CAMPAIGN WITH 'START CAMPAIGN AFTER APPROVAL' UNCHECKED
    campaign_settings_page.navigate_to_add_campaign_group()
    campaign_page.provide_name_and_type_info(campaign_data, duplicate_or_edit_campaign=False)
    campaign_page.provide_launch_date_and_budget_info(campaign_data, start_campaign_approval=True)
    campaign_page.provide_location_and_audiences_info(campaign_data)
    campaign_page.provide_landing_and_creatives_info(campaign_data)
    campaign_page.click_save_cancel_or_draft("SAVE")
    # SEARCH AND APPROVE THE CAMPAIGN
    campaign_settings_page.search_and_click_on_campaign_name(campaign_data['name_and_type']['campaign_name'],
                                                             index=1)
    campaign_view.perform_action("Approve")
    campaign_approve.click_approve_button()
    campaign_approve.click_on_element(CampaignApproveLocators.ignore_button_locator)
    time.sleep(campaign_approve.FIVE_SEC_DELAY)
    # VERIFY THAT THE CAMPAIGN'S STATUS IS 'STOPPED'
    campaign_settings_page.search_and_click_on_campaign_name(campaign_data['name_and_type']['campaign_name'],
                                                             index=1, click_on_campaign_name=False)
    assert 'Sto.' in campaign_settings_page.get_stopped_status_text()
