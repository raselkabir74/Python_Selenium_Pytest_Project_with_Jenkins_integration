import json
import os

import pytest

from configurations import generic_modules, mysql
from pages.campaign.campaign_form import DspDashboardCampaignsForm
from pages.campaign.campaign_list import DspDashboardCampaignsList
from pages.campaign.campaign_settings_list import DspDashboardCampaignsSettings
from pages.campaign.campaign_view import DspDashboardCampaignView
from utils.compare import CompareUtils as CompareUtil


@pytest.mark.skipif("JENKINS_URL" in os.environ or mysql.mysql_connection_test(),
                    reason="Test need to be run manually and database connection need to be established")
def test_add_campaign_ingame(login_by_user_type):
    config, driver = login_by_user_type
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_view = DspDashboardCampaignView(driver)
    campaign_list_page = DspDashboardCampaignsList(driver)
    # PROVIDED CAMPAIGN DATA IN GUI
    with open('assets/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['name_and_type']['campaign_name'] = campaign_data['name_and_type'][
                                                          'campaign_name'] + generic_modules.get_random_string(5)
    campaign_data['name_and_type']['campaign_type'] = "In-Game"
    campaign_data['platforms_telco_and_devices']['ad_placement_type'] = "App"
    campaign_data['optimisations_deals_and_packages']['ad_exchange_checkbox'] = ["AdInMo", "Anzu", "Gadsme", "Adverty"]
    # CAMPAIGN CREATION
    campaign_settings_page.navigate_to_add_campaign_group()
    campaign_page.provide_campaign_data_and_save(campaign_data, "Save", ingame= True)
    assert "Saved successfully." in campaign_settings_page.get_success_message()
    # DATA VERIFICATION
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action(campaign_data['name_and_type']['campaign_name'], 'Edit')
    pulled_campaign_data_gui = campaign_page.get_campaign_information_with_multiple_attempt(campaign_data, ingame= True)
    print("pulled_campaign_data_gui", generic_modules.ordered(pulled_campaign_data_gui))
    print("campaign_data           ", generic_modules.ordered(campaign_data))
    assert "All data verification is successful" == CompareUtil.verify_data(pulled_campaign_data_gui, campaign_data)

    # CAMPAIGN CLEAN UP
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action(campaign_data['name_and_type']['campaign_name'], 'Delete')
    assert "Campaign deleted successfully" in campaign_view.get_success_message()