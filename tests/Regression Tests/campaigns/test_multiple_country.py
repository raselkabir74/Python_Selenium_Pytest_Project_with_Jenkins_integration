import json
import os

import pytest

from configurations import generic_modules, mysql
from pages.campaign.campaign_form import DspDashboardCampaignsForm
from pages.campaign.campaign_settings_list import DspDashboardCampaignsSettings
from pages.campaign.campaign_view import DspDashboardCampaignView
from utils.compare import CompareUtils as CompareUtil


@pytest.mark.skipif("JENKINS_URL" in os.environ or mysql.mysql_connection_test(),
                    reason="Test need to be run manually and database connection need to be established")
def test_multiple_country_multiple_campaign(login_by_user_type):
    config, driver = login_by_user_type
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_view = DspDashboardCampaignView(driver)
    # PROVIDED CAMPAIGN DATA IN GUI
    with open('assets/regression_tests/campaign_multiple_country_data.json') as json_file:
        campaign_multiple_country_data = json.load(json_file)
    campaign_name = campaign_multiple_country_data['name_and_type']['campaign_name'] + generic_modules.get_random_string(5)
    campaign_multiple_country_data['name_and_type']['campaign_name'] = campaign_name
    # CREATED MULTIPLE CAMPAIGNS WITH MULTIPLE COUNTRIES
    campaign_settings_page.navigate_to_add_campaign_group()
    campaign_page.provide_campaign_data_and_save_for_multiple_platform_and_multiple_country(campaign_multiple_country_data, "Save", multi_country=True)
    assert "Saved successfully." in campaign_settings_page.get_success_message()
    # DATA VERIFICATION
    campaign_settings_page.select_all_status()
    multiple_country_name_data = [" - BD/Eskimi", " - AF/Eskimi"]
    for country_name_in_campaign in multiple_country_name_data:
        index = multiple_country_name_data.index(country_name_in_campaign)
        if country_name_in_campaign == " - BD/Eskimi":
            index = index + 1
            name_to_search_with = campaign_name + country_name_in_campaign
            campaign_settings_page.search_and_click_on_campaign_name(name_to_search_with, index)
            campaign_view.perform_action("Edit")
            pulled_campaign_data_gui = campaign_page.get_campaign_information_with_multiple_attempt(
                campaign_multiple_country_data, multi_country = True)
            campaign_multiple_country_data['name_and_type']['campaign_name'] = campaign_name + country_name_in_campaign
            campaign_multiple_country_data['location_and_audiences']['country_name'] = "Bangladesh"
            campaign_multiple_country_data['location_and_audiences']['city_name'] = "Dhaka - Bangladesh"
            campaign_multiple_country_data['location_and_audiences']['state_name'] = "Dhaka division - Bangladesh"
            campaign_multiple_country_data['platforms_telco_and_devices']['mobile_operator'] = "Robi - Bangladesh"
            campaign_multiple_country_data['platforms_telco_and_devices']['multiple_operation_sim_card'] = "Robi - Bangladesh"
            campaign_multiple_country_data['platforms_telco_and_devices']['operator_churn'] = "Robi - Bangladesh"
            print("multiple country data", generic_modules.ordered(campaign_multiple_country_data))
            print("pulled data gui", generic_modules.ordered(pulled_campaign_data_gui))
            assert "All data verification is successful" == CompareUtil.verify_data(pulled_campaign_data_gui,
                                                                                    campaign_multiple_country_data)
            # CLEAN UP
            campaign_settings_page.move_to_campaign_settings_page()
            campaign_settings_page.search_and_click_on_campaign_name(name_to_search_with, index)
            campaign_view.perform_action("Delete")
            assert "Campaign deleted successfully" in campaign_view.get_success_message()
            campaign_settings_page.move_to_campaign_settings_page()
        elif country_name_in_campaign == " - AF/Eskimi":
            index = multiple_country_name_data.index(country_name_in_campaign)
            name_to_search_with = campaign_name + country_name_in_campaign
            campaign_settings_page.search_and_click_on_campaign_name(name_to_search_with, index)
            campaign_view.perform_action("Edit")
            pulled_campaign_data_gui = campaign_page.get_campaign_information_with_multiple_attempt(
                    campaign_multiple_country_data, multi_country = True)
            campaign_multiple_country_data['name_and_type']['campaign_name'] = campaign_name + country_name_in_campaign
            campaign_multiple_country_data['location_and_audiences']['country_name'] = "Afghanistan"
            campaign_multiple_country_data['location_and_audiences']['city_name'] = "Kunduz - Afghanistan"
            campaign_multiple_country_data['location_and_audiences']['state_name'] = "Badakhshan - Afghanistan"
            campaign_multiple_country_data['platforms_telco_and_devices']['mobile_operator'] = "AWCC - Afghanistan"
            campaign_multiple_country_data['platforms_telco_and_devices']['multiple_operation_sim_card'] = "AWCC - Afghanistan"
            campaign_multiple_country_data['platforms_telco_and_devices']['operator_churn'] = "AWCC - Afghanistan"
            print("multiple country data", generic_modules.ordered(campaign_multiple_country_data))
            print("pulled data gui", generic_modules.ordered(pulled_campaign_data_gui))
            assert "All data verification is successful" == CompareUtil.verify_data(pulled_campaign_data_gui,
                                                                                        campaign_multiple_country_data)
            # CLEAN UP
            campaign_settings_page.move_to_campaign_settings_page()
            campaign_settings_page.search_and_click_on_campaign_name(name_to_search_with, index)
            campaign_view.perform_action("Delete")
            assert "Campaign deleted successfully" in campaign_view.get_success_message()




