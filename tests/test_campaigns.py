import json
import os

import pytest

from configurations import generic_modules, mysql
from pages.base_page import BasePage
from pages.campaign.campaign_approve_form import DspDashboardCampaignApprove
from pages.campaign.campaign_form import DspDashboardCampaignsForm
from pages.campaign.campaign_goal_form import DspDashboardCampaignGoal
from pages.campaign.campaign_list import DspDashboardCampaignsList
from pages.campaign.campaign_mass_duplicate_form import DspDashboardCampaignsMassDuplicate
from pages.campaign.campaign_mass_approve_form import DspDashboardCampaignsMassApprove
from pages.campaign.campaign_mass_edit_form import DspDashboardCampaignsMassEdit
from pages.campaign.campaign_settings_list import DspDashboardCampaignsSettings
from pages.campaign.campaign_view import DspDashboardCampaignView
from pages.sidebar.sidebar import DashboardSidebarPage
from utils.campaigns import CampaignUtils as CampaignUtil
from utils.compare import CompareUtils as CompareUtil


@pytest.mark.skipif("JENKINS_URL" in os.environ or mysql.mysql_connection_test(),
                    reason="Test need to be run manually and database connection need to be established")
def test_add_campaign(login_by_user_type):
    config, driver = login_by_user_type
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_view = DspDashboardCampaignView(driver)
    # PROVIDED CAMPAIGN DATA IN GUI
    with open('assets/campaign/campaign_data.json') as json_file:
        campaign_data = json.load(json_file)
    campaign_data['name_and_type']['campaign_name'] = campaign_data['name_and_type'][
                                                          'campaign_name'] + generic_modules.get_random_string(5)
    # EXPECTED DB DATA
    with open('assets/campaign/campaign_db_data.json') as json_file:
        expected_campaign_data_db = json.load(json_file)
    # CAMPAIGN CREATION
    campaign_settings_page.navigate_to_add_campaign_group()
    campaign_page.provide_campaign_data_and_save(campaign_data, "Save")
    assert "Saved successfully." in campaign_settings_page.get_success_message()
    # DATA VERIFICATION
    campaign_settings_page.select_all_status()
    campaign_settings_page.search_and_click_on_campaign_name(campaign_data['name_and_type']['campaign_name'],
                                                             index=1)
    campaign_view.perform_action("Edit")
    pulled_campaign_data_gui = campaign_page.get_campaign_information_with_multiple_attempt(campaign_data)
    pulled_campaign_data_db = CampaignUtil.pull_campaign_data_db(campaign_data['name_and_type']['campaign_name'])
    print("pulled_campaign_data_gui", generic_modules.ordered(pulled_campaign_data_gui))
    print("campaign_data           ", generic_modules.ordered(campaign_data))
    assert "All data verification is successful" == CompareUtil.verify_data(pulled_campaign_data_gui, campaign_data,
                                                                            pulled_campaign_data_db,
                                                                            expected_campaign_data_db,
                                                                            db_verification=True)
    # CAMPAIGN CLEAN UP
    campaign_settings_page.move_to_campaign_settings_page()
    campaign_settings_page.search_and_click_on_campaign_name(campaign_data['name_and_type']['campaign_name'],
                                                             index=1)
    campaign_view.perform_action("Delete")
    assert "Campaign deleted successfully" in campaign_view.get_success_message()


@pytest.mark.skipif("JENKINS_URL" in os.environ, reason="Test need to be run manually")
def test_duplicate_and_edit_campaign(login_by_user_type):
    config, driver = login_by_user_type
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    campaign_view = DspDashboardCampaignView(driver)

    # [START] DUPLICATE EXISTING CAMPAIGN
    # DUPLICATE CAMPAIGN DATA TO PROVIDE IN GUI
    with open('assets/campaign/campaign_duplicate_data.json') as json_file:
        campaign_duplicate_data = json.load(json_file)
    campaign_duplicate_data['name_and_type']['campaign_name'] = campaign_duplicate_data['name_and_type'][
                                                                    'campaign_name'] + \
                                                                generic_modules.get_random_string(5)
    # DUPLICATE EXISTING CAMPAIGN
    campaign_settings_page.select_all_status()
    campaign_settings_page.search_and_click_on_campaign_name(
        config['campaign']['campaign-name-for-single-edit-and-duplicate'],
        index=1)
    campaign_view.perform_action("Duplicate")
    campaign_page.provide_campaign_data_and_save(campaign_duplicate_data, "Save", duplicate_campaign=True)
    assert "Saved successfully." in campaign_settings_page.get_success_message()
    # DATA VERIFICATION
    campaign_settings_page.move_to_campaign_settings_page()
    campaign_settings_page.select_all_status()
    campaign_settings_page.search_and_click_on_campaign_name(campaign_duplicate_data['name_and_type']['campaign_name'],
                                                             index=1)
    campaign_view.perform_action("Edit")
    pulled_campaign_data_gui = campaign_page.get_campaign_information_with_multiple_attempt(campaign_duplicate_data)
    print("pulled campaign data gui", generic_modules.ordered(pulled_campaign_data_gui))
    print("campaign duplicate data ", generic_modules.ordered(campaign_duplicate_data))
    assert "All data verification is successful" == CompareUtil.verify_data(pulled_campaign_data_gui,
                                                                            campaign_duplicate_data)

    # [END] DUPLICATE EXISTING CAMPAIGN

    # [START] EDIT EXISTING CAMPAIGN
    # EDIT CAMPAIGN DATA TO PROVIDE IN GUI
    with open('assets/campaign/campaign_edit_data.json') as json_file:
        campaign_edit_data = json.load(json_file)
    campaign_edit_data['name_and_type']['campaign_name'] = campaign_edit_data['name_and_type'][
                                                               'campaign_name'] + generic_modules.get_random_string(5)
    # EDIT EXISTING CAMPAIGN
    campaign_settings_page.move_to_campaign_settings_page()
    campaign_settings_page.select_all_status()
    campaign_settings_page.search_and_click_on_campaign_name(campaign_duplicate_data['name_and_type']['campaign_name'],
                                                             index=1)
    campaign_view.perform_action("Edit")
    campaign_page.provide_campaign_data_and_save(campaign_edit_data, "Save", edit_campaign=True)
    assert "Saved successfully." in campaign_settings_page.get_success_message()
    # DATA VERIFICATION
    campaign_settings_page.move_to_campaign_settings_page()
    campaign_settings_page.search_and_click_on_campaign_name(campaign_edit_data['name_and_type']['campaign_name'],
                                                             index=1)
    campaign_view.perform_action("Edit")
    pulled_edited_campaign_data_gui = campaign_page.get_campaign_information_with_multiple_attempt(campaign_edit_data)
    print("pulled campaign data gui", generic_modules.ordered(pulled_campaign_data_gui))
    print("campaign edit data      ", generic_modules.ordered(campaign_edit_data))
    assert "All data verification is successful" == CompareUtil.verify_data(pulled_edited_campaign_data_gui,
                                                                            campaign_edit_data)
    # CAMPAIGN CLEAN UP
    campaign_settings_page.move_to_campaign_settings_page()
    campaign_settings_page.search_and_click_on_campaign_name(campaign_edit_data['name_and_type']['campaign_name'],
                                                             index=1)
    campaign_view.perform_action("Delete")
    assert "Campaign deleted successfully" in campaign_view.get_success_message()
    # [END] EDIT EXISTING CAMPAIGN


@pytest.mark.skipif("JENKINS_URL" in os.environ, reason="Test need to be run manually")
def test_campaign_approve(login_by_user_type):
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
    campaign_settings_page.search_and_click_on_campaign_name(campaign['name'],
                                                             index=1)
    campaign_view.perform_action("Approve")
    campaign_approve_form.approve_campaign(provided_campaign_approve_data)
    # VERIFY THE DATA
    campaign_settings_page.select_all_status()
    campaign_settings_page.search_and_click_on_campaign_name(campaign['name'],
                                                             index=1)
    campaign_view.perform_action("Approve")
    assert "Pending" not in campaign_approve_form.get_campaign_status()
    pulled_campaign_approve_data = campaign_approve_form.get_campaign_approve_data()
    print("gui data", generic_modules.ordered(pulled_campaign_approve_data))
    print("given data", generic_modules.ordered(provided_campaign_approve_data))
    assert "All data verification is successful" == CompareUtil.verify_data(pulled_campaign_approve_data,
                                                                            provided_campaign_approve_data)
    # CAMPAIGN CLEAN UP
    campaign_approve_form.click_delete_button()
    assert "Campaign deleted" in campaign_list_page.get_success_message()


@pytest.mark.skipif("JENKINS_URL" in os.environ, reason="Test need to be run manually")
def test_campaign_mass_duplicate_and_edit(login_by_user_type):
    config, driver = login_by_user_type
    base_page = BasePage(driver)
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_list_page = DspDashboardCampaignsList(driver)
    campaign_mass_duplicate_page = DspDashboardCampaignsMassDuplicate(driver)
    campaign_mass_edit_page = DspDashboardCampaignsMassEdit(driver)

    # [START] MASS DUPLICATE EXISTING CAMPAIGNS
    # CAMPAIGN MASS DUPLICATE DATA TO PROVIDE IN GUI
    with open('assets/campaign/campaign_mass_duplicate_data.json') as json_file:
        campaign_mass_duplicate_data = json.load(json_file)
    # MASS DUPLICATE EXISTING CAMPAIGNS
    campaign_name_list_before_mass_duplicate = CampaignUtil.process_campaign_name(campaign_list=config['campaign'],
                                                                                  operation="before mass duplicate operation")
    campaign_name_list = CampaignUtil.process_campaign_name(campaign_list=config['campaign'],
                                                            operation="mass duplicate and edit")
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    campaign_list_page.search_and_action(config['campaign']['campaign-name-prefix-for-mass-edit-and-duplicate'])
    for campaign_name in campaign_name_list_before_mass_duplicate:
        campaign_list_page.check_uncheck_campaign_list_grid_row_checkbox(campaign_name=campaign_name,
                                                                         check_the_checkbox=True)
    campaign_list_page.select_item_from_campaign_multi_action_menu("Mass duplicate campaign",
                                                                   switch_to_new_window=True)
    campaign_mass_duplicate_page.provide_campaign_mass_duplicate_data_and_save(campaign_name_list)
    assert "Successfully created campaigns." in campaign_list_page.get_success_message()
    # DATA VERIFICATION
    for campaign_name in campaign_name_list:
        campaign_mass_duplicate_data['name_and_type']['campaign_name'] = campaign_name
        campaign_list_page.search_and_action(campaign_name, "Edit")
        pulled_mass_duplicate_campaign_data_gui = campaign_page.get_campaign_information_with_multiple_attempt(
            campaign_mass_duplicate_data)
        print("givengui data", generic_modules.ordered(pulled_mass_duplicate_campaign_data_gui))
        print("campaign data", generic_modules.ordered(campaign_mass_duplicate_data))
        assert "All data verification is successful" == CompareUtil.verify_data(pulled_mass_duplicate_campaign_data_gui,
                                                                                campaign_mass_duplicate_data)
    base_page.close_the_current_window_and_back_to_previous_window()
    # [END] MASS DUPLICATE EXISTING CAMPAIGNS

    # [START] MASS EDIT EXISTING CAMPAIGNS
    # EDIT CAMPAIGN DATA TO PROVIDE IN GUI
    with open('assets/campaign/campaign_mass_edit_data.json') as json_file:
        campaign_mass_edit_data = json.load(json_file)
    # EDIT EXISTING CAMPAIGNS
    campaign_name_list_to_edit = CampaignUtil.process_campaign_name(campaign_list=config['campaign'],
                                                                    operation="mass duplicate and edit")
    campaign_list_page.search_and_action(config['campaign']['campaign-name-prefix-after-mass-duplicate'],
                                         force_reload=True)
    for campaign_name in campaign_name_list:
        campaign_list_page.check_uncheck_campaign_list_grid_row_checkbox(campaign_name=campaign_name,
                                                                         check_the_checkbox=True)
    campaign_list_page.select_item_from_campaign_multi_action_menu("Mass edit campaign", switch_to_new_window=True)
    campaign_mass_edit_page.provide_campaign_mass_edit_data_and_save(campaign_name_list_to_edit,
                                                                     campaign_mass_edit_data)
    assert "Changes saved successfully" in campaign_list_page.get_success_message()
    # DATA VERIFICATION
    for campaign_name in campaign_name_list_to_edit:
        campaign_mass_edit_data['name_and_type']['campaign_name'] = campaign_name
        campaign_list_page.search_and_action(campaign_name, "Edit")
        pulled_mass_edit_campaign_data_gui = campaign_page.get_campaign_information_with_multiple_attempt(
            campaign_mass_edit_data)
        print("givengui data", generic_modules.ordered(pulled_mass_edit_campaign_data_gui))
        print("campaign data", generic_modules.ordered(campaign_mass_edit_data))
        assert "All data verification is successful" == CompareUtil.verify_data(pulled_mass_edit_campaign_data_gui,
                                                                                campaign_mass_edit_data)
    # CAMPAIGN CLEAN UP
    base_page.close_the_current_window_and_back_to_previous_window()
    campaign_list_page.search_and_action(config['campaign']['campaign-name-prefix-after-mass-duplicate'],
                                         force_reload=True)
    for campaign_name in campaign_name_list_to_edit:
        campaign_list_page.check_uncheck_campaign_list_grid_row_checkbox(campaign_name=campaign_name,
                                                                         check_the_checkbox=True)
    campaign_list_page.select_item_from_campaign_multi_action_menu("Delete")
    assert "Campaign deleted successfully" in campaign_list_page.get_success_message()
    # [END] MASS EDIT EXISTING CAMPAIGNS


@pytest.mark.skipif("JENKINS_URL" in os.environ, reason="Test need to be run manually")
def test_campaign_mass_approve(login_by_user_type):
    config, driver = login_by_user_type
    campaign_list_page = DspDashboardCampaignsList(driver)
    campaign_mass_approve_page = DspDashboardCampaignsMassApprove(driver)
    campaign_approve_form = DspDashboardCampaignApprove(driver)
    # CAMPAIGN MASS APPROVE DATA TO PROVIDE IN GUI
    with open('assets/campaign/campaign_mass_approve_data.json') as json_file:
        campaign_mass_approve_data = json.load(json_file)
    # CREATE CAMPAIGN BY API
    campaign_name_list = CampaignUtil.process_campaign_name(campaign_list=config['campaign-mass-approve'])
    for campaign_name in campaign_name_list:
        CampaignUtil.create_campaign_by_api(config, mass_campaign_name=campaign_name)
    campaign_list_page.reload_campaign_list_page()
    campaign_list_page.select_all_status()
    # CAMPAIGN MASS APPROVE
    campaign_mass_approve_data = CampaignUtil.process_campaign_approve_data(campaign_mass_approve_data)
    campaign_list_page.search_and_action(config['campaign-mass-approve']['campaign-name-prefix-for-mass-approve'])
    for campaign_name in campaign_name_list:
        campaign_list_page.check_uncheck_campaign_list_grid_row_checkbox(campaign_name=campaign_name,
                                                                         check_the_checkbox=True)
    campaign_list_page.select_item_from_campaign_multi_action_menu("Mass approve campaign", switch_to_new_window=True)
    campaign_mass_approve_page.provide_campaign_mass_approve_data_and_save(campaign_name_list,
                                                                           campaign_mass_approve_data)
    assert "Successfully approved campaigns." in campaign_list_page.get_success_message()
    # VERIFY DATA
    campaign_list_page.select_all_status()
    for campaign_name in campaign_name_list:
        campaign_list_page.search_and_action(campaign_name, "Approve")
        assert "Pending" not in campaign_approve_form.get_campaign_status()
        pulled_campaign_approve_data = campaign_approve_form.get_campaign_approve_data(mass_approve=True)
        print(campaign_name)
        print("guidata", generic_modules.ordered(pulled_campaign_approve_data))
        print("givendata", generic_modules.ordered(campaign_mass_approve_data))
        assert "All data verification is successful" == CompareUtil.verify_data(pulled_campaign_approve_data,
                                                                                campaign_mass_approve_data)
        campaign_list_page.reload_campaign_list_page()
    # CAMPAIGN CLEAN UP
    campaign_list_page.search_and_action(config['campaign-mass-approve']['campaign-name-prefix-for-mass-approve'])
    for campaign_name in campaign_name_list:
        campaign_list_page.check_uncheck_campaign_list_grid_row_checkbox(campaign_name=campaign_name,
                                                                         check_the_checkbox=True)
    campaign_list_page.select_item_from_campaign_multi_action_menu("Delete")
    assert "Campaign deleted successfully" in campaign_list_page.get_success_message()


@pytest.mark.skipif("JENKINS_URL" in os.environ, reason="Test need to be run manually")
def test_campaign_goal(login_by_user_type):
    config, driver = login_by_user_type
    campaign_list_page = DspDashboardCampaignsList(driver)
    campaign_goal_form = DspDashboardCampaignGoal(driver)

    with open('assets/campaign/campaign_goal_data.json') as json_file:
        provided_campaign_goal_data = json.load(json_file)
    # CREATE CAMPAIGN BY API
    campaign = CampaignUtil.create_campaign_by_api(config)
    # CAMPAIGN GOAL
    campaign_list_page.search_and_action(campaign['name'], "Campaign goals", force_reload=True)
    campaign_goal_form.provide_campaign_goal_info(provided_campaign_goal_data)
    assert "Campaign goals saved successfully!" in campaign_list_page.get_success_message()
    # VERIFY THE DATA
    campaign_list_page.search_and_action(campaign['name'], "Campaign goals", force_reload=True)
    pulled_campaign_goal_data = campaign_goal_form.get_campaign_goal_information()
    assert "All data verification is successful" == CompareUtil.verify_data(pulled_campaign_goal_data,
                                                                            provided_campaign_goal_data)
    # CAMPAIGN CLEAN UP
    campaign_list_page.search_and_action(campaign['name'], "Delete", force_reload=True)
    assert "Campaign deleted successfully" in campaign_list_page.get_success_message()


@pytest.mark.skipif("JENKINS_URL" in os.environ, reason="Test need to be run manually")
def test_campaign_settings(login_by_user_type):
    config, driver = login_by_user_type
    sidebar_navigation = DashboardSidebarPage(driver)
    campaign_list_page = DspDashboardCampaignsList(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    with open('assets/campaign/campaign_settings_data.json') as json_file:
        campaign_settings_data = json.load(json_file)
    campaign_settings_data['name'] = campaign_settings_data['name'] + generic_modules.get_random_string(5)
    # CREATE CAMPAIGN BY API
    campaign = CampaignUtil.create_campaign_by_api(config)
    # UPDATE DATA IN CAMPAIGN SETTINGS PAGE
    sidebar_navigation.navigate_to_campaign_settings()
    campaign_settings_page.update_campaign_setting_data_single(campaign['campaignId'], campaign_settings_data)
    # VERIFY FATA
    pulled_campaign_data = campaign_settings_page.get_campaign_data(campaign['campaignId'])
    assert "All data verification is successful" == CompareUtil.verify_data(pulled_campaign_data,
                                                                            campaign_settings_data)
    # CAMPAIGN CLEAN UP
    campaign_list_page.search_and_action(campaign['campaignId'], "Delete", force_reload=True)
    assert "Campaign deleted successfully" in campaign_list_page.get_success_message()
