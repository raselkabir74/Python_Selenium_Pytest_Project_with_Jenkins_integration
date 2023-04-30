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
def test_multiple_platform_multiple_campaign(login_by_user_type):
    config, driver = login_by_user_type
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_view = DspDashboardCampaignView(driver)
    # PROVIDED CAMPAIGN DATA IN GUI
    with open('assets/regression_tests/campaign_multiple_platform_data.json') as json_file:
        campaign_mandatory_data = json.load(json_file)
    campaign_name = campaign_mandatory_data['name_and_type']['campaign_name'] + generic_modules.get_random_string(5)
    campaign_mandatory_data['name_and_type']['campaign_name'] = campaign_name
    # CREATED MULTIPLE CAMPAIGNS WITH MULTIPLE PLATFORMS
    campaign_settings_page.navigate_to_add_campaign_group()
    campaign_page.provide_campaign_data_and_save_for_multiple_platform_and_multiple_country(campaign_mandatory_data, "Save",
                                                 multi_platform=True, multi_country=False)
    assert "Saved successfully." in campaign_settings_page.get_success_message()
    # DATA VERIFICATION
    campaign_settings_page.select_all_status()
    multiple_platform_name_data = [" - BD/Facebook", " - BD/Eskimi", " - BD/Youtube", " - BD/Adwords", " - BD/Tiktok"]
    for platform_name_in_campaign in multiple_platform_name_data:
        index = multiple_platform_name_data.index(platform_name_in_campaign)
        if platform_name_in_campaign == " - BD/Facebook":
            index = index + 1
            name_to_search_with = campaign_name + platform_name_in_campaign
            campaign_settings_page.search_and_click_on_campaign_name(name_to_search_with, index)
            campaign_view.perform_action("Edit")
            pulled_campaign_data_gui = campaign_page.get_campaign_information_with_multiple_attempt(
                campaign_mandatory_data, multi_platform_or_only_mandatory=True)
            campaign_mandatory_data['name_and_type']['campaign_name'] = campaign_name + platform_name_in_campaign
            campaign_mandatory_data['name_and_type']['platform_type'] = "Facebook"
            print("mandatory data", generic_modules.ordered(campaign_mandatory_data))
            print("pulled data gui", generic_modules.ordered(pulled_campaign_data_gui))
            assert "All data verification is successful" == CompareUtil.verify_data(pulled_campaign_data_gui,
                                                                                    campaign_mandatory_data)
            # CLEAN UP
            campaign_settings_page.move_to_campaign_settings_page()
            campaign_settings_page.search_and_click_on_campaign_name(name_to_search_with, index)
            campaign_view.perform_action("Delete")
            assert "Campaign deleted successfully" in campaign_view.get_success_message()
            campaign_settings_page.move_to_campaign_settings_page()
        elif platform_name_in_campaign == " - BD/Eskimi":
            index = multiple_platform_name_data.index(platform_name_in_campaign)
            name_to_search_with = campaign_name+platform_name_in_campaign
            campaign_settings_page.search_and_click_on_campaign_name(name_to_search_with, index)
            campaign_view.perform_action("Edit")
            pulled_campaign_data_gui = campaign_page.get_campaign_information_with_multiple_attempt(
                    campaign_mandatory_data, multi_platform_or_only_mandatory=True)
            campaign_mandatory_data['name_and_type']['campaign_name'] = campaign_name + platform_name_in_campaign
            campaign_mandatory_data['name_and_type']['platform_type'] = "Eskimi"
            print("mandatory data", generic_modules.ordered(campaign_mandatory_data))
            print("pulled data gui", generic_modules.ordered(pulled_campaign_data_gui))
            assert "All data verification is successful" == CompareUtil.verify_data(pulled_campaign_data_gui,
                                                                                        campaign_mandatory_data)
            # CLEAN UP
            campaign_settings_page.move_to_campaign_settings_page()
            campaign_settings_page.search_and_click_on_campaign_name(name_to_search_with, index)
            campaign_view.perform_action("Delete")
            assert "Campaign deleted successfully" in campaign_view.get_success_message()
            campaign_settings_page.move_to_campaign_settings_page()
        elif platform_name_in_campaign == " - BD/Youtube":
            index = index - 1
            name_to_search_with = campaign_name + platform_name_in_campaign
            campaign_settings_page.search_and_click_on_campaign_name(name_to_search_with, index)
            campaign_view.perform_action("Edit")
            pulled_campaign_data_gui = campaign_page.get_campaign_information_with_multiple_attempt(
                campaign_mandatory_data, multi_platform_or_only_mandatory=True)
            campaign_mandatory_data['name_and_type']['campaign_name'] = campaign_name + platform_name_in_campaign
            campaign_mandatory_data['name_and_type']['platform_type'] = "Youtube"
            print("mandatory data", generic_modules.ordered(campaign_mandatory_data))
            print("pulled data gui", generic_modules.ordered(pulled_campaign_data_gui))
            assert "All data verification is successful" == CompareUtil.verify_data(pulled_campaign_data_gui,
                                                                                    campaign_mandatory_data)
            # CLEAN UP
            campaign_settings_page.move_to_campaign_settings_page()
            campaign_settings_page.search_and_click_on_campaign_name(name_to_search_with, index)
            campaign_view.perform_action("Delete")
            assert "Campaign deleted successfully" in campaign_view.get_success_message()
            campaign_settings_page.move_to_campaign_settings_page()
        elif platform_name_in_campaign == " - BD/Adwords":
            index = index - 2
            name_to_search_with = campaign_name + platform_name_in_campaign
            campaign_settings_page.search_and_click_on_campaign_name(name_to_search_with, index)
            campaign_view.perform_action("Edit")
            pulled_campaign_data_gui = campaign_page.get_campaign_information_with_multiple_attempt(
                campaign_mandatory_data, multi_platform_or_only_mandatory=True)
            campaign_mandatory_data['name_and_type']['campaign_name'] = campaign_name + platform_name_in_campaign
            campaign_mandatory_data['name_and_type']['platform_type'] = "Adwords"
            print("mandatory data", generic_modules.ordered(campaign_mandatory_data))
            print("pulled data gui", generic_modules.ordered(pulled_campaign_data_gui))
            assert "All data verification is successful" == CompareUtil.verify_data(pulled_campaign_data_gui,
                                                                                    campaign_mandatory_data)
            # CLEAN UP
            campaign_settings_page.move_to_campaign_settings_page()
            campaign_settings_page.search_and_click_on_campaign_name(name_to_search_with, index)
            campaign_view.perform_action("Delete")
            assert "Campaign deleted successfully" in campaign_view.get_success_message()
            campaign_settings_page.move_to_campaign_settings_page()
        elif platform_name_in_campaign == " - BD/Tiktok":
            index = index - 3
            name_to_search_with = campaign_name + platform_name_in_campaign
            campaign_settings_page.search_and_click_on_campaign_name(name_to_search_with, index)
            campaign_view.perform_action("Edit")
            pulled_campaign_data_gui = campaign_page.get_campaign_information_with_multiple_attempt(
                campaign_mandatory_data, multi_platform_or_only_mandatory=True)
            campaign_mandatory_data['name_and_type']['campaign_name'] = campaign_name + platform_name_in_campaign
            campaign_mandatory_data['name_and_type']['platform_type'] = "Tiktok"
            print("mandatory data", generic_modules.ordered(campaign_mandatory_data))
            print("pulled data gui", generic_modules.ordered(pulled_campaign_data_gui))
            assert "All data verification is successful" == CompareUtil.verify_data(pulled_campaign_data_gui,
                                                                                    campaign_mandatory_data)
            # CLEAN UP
            campaign_settings_page.move_to_campaign_settings_page()
            campaign_settings_page.search_and_click_on_campaign_name(name_to_search_with, index)
            campaign_view.perform_action("Delete")
            assert "Campaign deleted successfully" in campaign_view.get_success_message()
            campaign_settings_page.move_to_campaign_settings_page()

