import json
import os
import time

import pytest

from configurations import generic_modules, mysql
from locators.campaign.campaign_form_locator import CampaignFormLocators
from pages.campaign.campaign_form import DspDashboardCampaignsForm
from pages.campaign.campaign_list import DspDashboardCampaignsList
from pages.campaign.campaign_settings_list import DspDashboardCampaignsSettings
from pages.campaign.campaign_view import DspDashboardCampaignView
from utils.compare import CompareUtils as CompareUtil


@pytest.mark.skipif("JENKINS_URL" in os.environ or mysql.mysql_connection_test(),
                    reason="Test need to be run manually and database connection need to be established")
def test_campaign_cancel_or_draft_functionality(login_by_user_type):
    config, driver = login_by_user_type
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_list_page = DspDashboardCampaignsList(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_view = DspDashboardCampaignView(driver)
    # PROVIDED CAMPAIGN DATA IN GUI
    with open('assets/regression_tests/campaign_mandatory_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['name_and_type']['campaign_name'] = campaign_data['name_and_type'][
                                                          'campaign_name'] + generic_modules.get_random_string(5)

    campaign_settings_page.navigate_to_add_campaign_group()
    campaign_page.provide_name_and_type_info(campaign_data)
    campaign_page.provide_launch_date_and_budget_info(campaign_data)
    campaign_page.click_on_element(CampaignFormLocators.button_group_locator)
    time.sleep(2)
    campaign_page.click_on_element(CampaignFormLocators.cancel_button_locator)
    assert "Campaign settings" in campaign_settings_page.get_campaign_settings_link_text()
    campaign_settings_page.navigate_to_add_campaign_group()
    campaign_page.provide_name_and_type_info(campaign_data)
    campaign_page.select_from_modal(campaign_data['location_and_audiences']['country_name'],
                                   CampaignFormLocators.country_label)
    campaign_page.click_save_cancel_or_draft("Draft")
    assert "Campaign saved successfully." in campaign_settings_page.get_success_message()
    # DRAFT STATUS VERIFICATION
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action(campaign_data['name_and_type']['campaign_name'], 'None')
    assert "Dra." in campaign_list_page.get_draft_status_text()
    campaign_list_page.search_and_action(campaign_data['name_and_type']['campaign_name'], 'Edit')
    campaign_page.provide_launch_date_and_budget_info(campaign_data)
    campaign_page.provide_landing_and_creatives_info(campaign_data)
    campaign_page.click_save_cancel_or_draft("Save")
    # DATA VERIFICATION
    campaign_list_page.search_and_action(campaign_data['name_and_type']['campaign_name'], 'Edit')
    pulled_campaign_data_gui = campaign_page.get_campaign_information_with_multiple_attempt(campaign_data, multi_platform_or_only_mandatory=True)
    print("pulled_campaign_data_gui", generic_modules.ordered(pulled_campaign_data_gui))
    print("campaign_data           ", generic_modules.ordered(campaign_data))
    assert "All data verification is successful" == CompareUtil.verify_data(pulled_campaign_data_gui, campaign_data)
    # CLEAN UP
    campaign_list_page.search_and_action(campaign_data['name_and_type']['campaign_name'], 'Delete')
    assert "Campaign deleted successfully" in campaign_list_page.get_success_message()




