import json

from pages.campaign.campaign_form import DspDashboardCampaignsForm
from pages.campaign.campaign_settings_list import DspDashboardCampaignsSettings
from locators.campaign.campaign_form_locator import CampaignFormLocators


def test_campaign_purpose(login_by_user_type):
    config, driver = login_by_user_type
    campaign_page = DspDashboardCampaignsForm(driver)
    campaign_settings_page = DspDashboardCampaignsSettings(driver)
    # PROVIDED CAMPAIGN DATA IN GUI
    with open('assets/regression_tests/campaign_regression_data.json') as json_file:
        campaign_regression_data = json.load(json_file)
    campaign_settings_page.navigate_to_add_campaign_group()
    # VERIFY CAMPAIGN PURPOSE AND PRIMARY OPERATOR SELECTION
    campaign_page.select_from_modal(campaign_regression_data['location_and_audiences']['country_name'],
                                    CampaignFormLocators.country_label)
    campaign_page.click_on_element(CampaignFormLocators.campaign_purpose_section_locator)
    campaign_page.select_dropdown_value(CampaignFormLocators.campaign_purpose_label,
                                        dropdown_item=campaign_regression_data['campaign_purpose']['campaign_purpose'])
    campaign_page.select_dropdown_value(CampaignFormLocators.primary_operator_label,
                                        dropdown_item=campaign_regression_data['campaign_purpose']['primary_operator'])
    assert campaign_regression_data['campaign_purpose'][
               'campaign_purpose'] in campaign_page.get_text_using_tag_attribute(campaign_page.span_tag,
                                                                                 campaign_page.id_attribute,
                                                                                 CampaignFormLocators.campaign_purpose_field_id)
    assert campaign_regression_data['campaign_purpose'][
               'primary_operator'] in campaign_page.get_text_using_tag_attribute(campaign_page.span_tag,
                                                                                 campaign_page.id_attribute,
                                                                                 CampaignFormLocators.primary_operator_field_id)
    # VERIFY ALERT MESSAGE IN CAMPAIGN PURPOSE FOR MULTIPLE COUNTRY
    campaign_regression_data['location_and_audiences']['country_name'] = "Bangladesh"
    campaign_page.select_from_modal(campaign_regression_data['location_and_audiences']['country_name'],
                                    CampaignFormLocators.country_label, click_uncheck_all=False)
    assert "Select one country to set campaign purpose" in campaign_page.get_element_text(
        CampaignFormLocators.campaign_purpose_warning_message_locator)
