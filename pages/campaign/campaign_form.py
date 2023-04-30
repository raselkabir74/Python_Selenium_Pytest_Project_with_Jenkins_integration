import os
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from configurations.generic_modules import step_printer
from locators.campaign.campaign_form_locator import CampaignFormLocators
from pages.base_page import BasePage

campaign_information = {'name_and_type': {}, 'launch_date_and_budget': {}, 'location_and_audiences': {},'campaign_purpose': {},
                        'platforms_telco_and_devices': {}, 'optimisations_deals_and_packages': {},
                        'landing_and_creatives': {}}


class DspDashboardCampaignsForm(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def provide_name_and_type_info(self, campaign_data, duplicate_or_edit_campaign=False, multi_platform=False, ingame=False):
        if multi_platform:
            platforms = campaign_data['name_and_type']['platform_type']
            for platform in platforms:
                self.click_on_element(CampaignFormLocators.platform_name.format(platform.lower()), locator_initialization=True)
        if duplicate_or_edit_campaign is False:
            creative_type = campaign_data['name_and_type']['creative_type']
            try:
                self.wait_for_presence_of_element(CampaignFormLocators.creative_type_dropdown_locator, self.HALF_MINUTE)
            finally:
                self.select_dropdown_value(CampaignFormLocators.type_label, dropdown_item=creative_type)
        if ingame:
            self.select_dropdown_value(CampaignFormLocators.campaign_type_label,
                                                campaign_data['name_and_type']['campaign_type'])
        self.wait_for_presence_of_element(CampaignFormLocators.creative_type_dropdown_locator, self.HALF_MINUTE)
        self.set_value_into_element(CampaignFormLocators.campaign_name_input_field_locator,
                                    campaign_data['name_and_type']['campaign_name'])

    def provide_launch_date_and_budget_info(self, campaign_data, duplicate_campaign=False, start_campaign_approval=False):
        self.select_specific_date_range(CampaignFormLocators.date_label, "7 Days")
        if duplicate_campaign is False:
            self.click_on_element(CampaignFormLocators.time_and_day_scheduling_locator)
            time.sleep(self.TWO_SEC_DELAY)
            self.click_on_element(CampaignFormLocators.specific_time_and_day_scheduling_locator)
            self.click_on_element(CampaignFormLocators.time_and_day_scheduling_save_button_locator)
            self.set_value_into_specific_input_field(CampaignFormLocators.bid_cpm_label,
                                                     campaign_data['launch_date_and_budget']['bid_cpm'])
            self.set_value_into_specific_input_field(CampaignFormLocators.total_budget_label,
                                                     campaign_data['launch_date_and_budget']['total_budget'])
            if start_campaign_approval:
                self.click_on_element(CampaignFormLocators.start_campaign_after_approval_locator)

    def provide_location_and_audiences_info(self, campaign_data, edit_campaign=False):
        if edit_campaign is False:
            self.select_from_modal(campaign_data['location_and_audiences']['country_name'],
                                   CampaignFormLocators.country_label)
            time.sleep(self.TWO_SEC_DELAY)
        # For city loading
        # CITY
        self.click_on_element(CampaignFormLocators.city_section_locator)
        self.wait_for_element_to_be_clickable(CampaignFormLocators.city_selection_locator)
        self.click_on_element(CampaignFormLocators.city_selection_locator)
        self.select_from_modal(search_text=campaign_data['location_and_audiences']['city_name'])
        # STATE
        time.sleep(self.TWO_SEC_DELAY)
        self.click_on_element(CampaignFormLocators.state_section_locator)
        self.wait_for_element_to_be_clickable(CampaignFormLocators.state_selection_locator)
        self.click_on_element(CampaignFormLocators.state_selection_locator)
        self.select_from_modal(search_text=campaign_data['location_and_audiences']['state_name'])
        # AUDIENCE
        time.sleep(self.TWO_SEC_DELAY)
        if edit_campaign is False:
            self.click_on_element(CampaignFormLocators.audience_section_locator)
        self.click_on_element(CampaignFormLocators.audience_include_selection_locator)
        self.select_from_modal(search_text=campaign_data['location_and_audiences']['audience_include'])
        time.sleep(self.TWO_SEC_DELAY)
        self.click_on_element(CampaignFormLocators.audience_exclude_selection_locator)
        self.select_from_modal(search_text=campaign_data['location_and_audiences']['audience_exclude'])
        # AGE
        if edit_campaign is False:
            self.click_on_element(CampaignFormLocators.demographic_section_locator)
        self.select_from_modal(campaign_data['location_and_audiences']['age'], CampaignFormLocators.age_label)
        # GENDER
        self.select_from_modal(campaign_data['location_and_audiences']['gender'],
                               CampaignFormLocators.gender_label)
        # LANGUAGE
        self.select_from_modal(campaign_data['location_and_audiences']['language'],
                               CampaignFormLocators.languages_label)
        # SEC (socio-economic class) groups
        self.select_from_modal(campaign_data['location_and_audiences']['sec'],
                               CampaignFormLocators.sec_socio_economic_class_groups_label)

    def provide_location_and_audiences_info_for_mul_platform_and_country(self, campaign_data, multi_platform=False,
                                                                         multi_country=False):
        if multi_platform is True:
            if multi_country is True:
                self.select_multiple_item_from_modal(campaign_data['location_and_audiences']['country_name'],
                                                     CampaignFormLocators.country_label)
            else:
                self.select_from_modal(campaign_data['location_and_audiences']['country_name'],
                                       CampaignFormLocators.country_label)
        else:
            self.select_multiple_item_from_modal(campaign_data['location_and_audiences']['country_name'],
                                                 CampaignFormLocators.country_label)
            time.sleep(self.TWO_SEC_DELAY)  # For city loading
            city_values = campaign_data['location_and_audiences']['city_name']
            time.sleep(self.TWO_SEC_DELAY)
            self.click_on_element(CampaignFormLocators.city_section_locator)
            for city in city_values:
                self.wait_for_element_to_be_clickable(CampaignFormLocators.city_selection_locator)
                self.click_on_element(CampaignFormLocators.city_selection_locator)
                self.select_from_modal_for_multiple_country(search_text=city)
            time.sleep(self.TWO_SEC_DELAY)
            state_values = campaign_data['location_and_audiences']['state_name']
            self.click_on_element(CampaignFormLocators.state_section_locator)
            for state in state_values:
                self.wait_for_element_to_be_clickable(CampaignFormLocators.state_selection_locator)
                self.click_on_element(CampaignFormLocators.state_selection_locator)
                self.select_from_modal_for_multiple_country(search_text=state)
            self.click_on_element(CampaignFormLocators.demographic_section_locator)
            time.sleep(self.TWO_SEC_DELAY)
            # AUDIENCE
            self.click_on_element(CampaignFormLocators.audience_section_locator)
            self.click_on_element(CampaignFormLocators.audience_include_selection_locator)
            self.select_from_modal(search_text=campaign_data['location_and_audiences']['audience_include'])
            time.sleep(self.TWO_SEC_DELAY)
            self.click_on_element(CampaignFormLocators.audience_exclude_selection_locator)
            self.select_from_modal(search_text=campaign_data['location_and_audiences']['audience_exclude'])
            # AGE
            self.select_from_modal(campaign_data['location_and_audiences']['age'], CampaignFormLocators.age_label)
            time.sleep(self.TWO_SEC_DELAY)
            # GENDER
            self.select_from_modal(campaign_data['location_and_audiences']['gender'],
                                   CampaignFormLocators.gender_label)
            # LANGUAGE
            self.select_from_modal(campaign_data['location_and_audiences']['language'],
                                   CampaignFormLocators.languages_label)
            # SEC (socio-economic class) groups
            self.select_from_modal(campaign_data['location_and_audiences']['sec'],
                                   CampaignFormLocators.sec_socio_economic_class_groups_label)
        time.sleep(self.TWO_SEC_DELAY)

    def provide_campaign_purpose_info(self, campaign_data, edit_campaign=False):
        if edit_campaign is False:
            self.click_on_element(CampaignFormLocators.campaign_purpose_section_locator)
        self.select_dropdown_value(CampaignFormLocators.campaign_purpose_label,
                                   dropdown_item=campaign_data['campaign_purpose']['campaign_purpose'])
        self.select_dropdown_value(CampaignFormLocators.primary_operator_label,
                                   dropdown_item=campaign_data['campaign_purpose']['primary_operator'])

    def provide_platforms_telco_and_devices_info(self, campaign_data, edit_campaign=False, multi_country=False):
        if edit_campaign is False:
            self.click_on_element(CampaignFormLocators.platforms_telco_devices_group_locator)
            self.wait_for_element_to_be_clickable(CampaignFormLocators.ad_placement_type_locator)
            self.click_on_element(CampaignFormLocators.ad_placement_type_locator)
        # PLACEMENT_TYPE
        self.check_uncheck_specific_checkbox("App", False)
        self.check_uncheck_specific_checkbox("Site", False)
        self.check_uncheck_specific_checkbox(campaign_data['platforms_telco_and_devices']['ad_placement_type'], True)
        # OPERATOR
        if multi_country is False:
            self.select_from_modal(campaign_data['platforms_telco_and_devices']['mobile_operator'],
                                   CampaignFormLocators.mobile_operators_isp_label)
        else:
            self.select_multiple_item_from_modal(campaign_data['platforms_telco_and_devices']['mobile_operator'],
                                                 CampaignFormLocators.mobile_operators_isp_label)
        # IP ADDRESSES/RANGES
        if edit_campaign is False:
            self.click_on_element(CampaignFormLocators.ip_ranges_section_locator)
        self.set_value_into_element(CampaignFormLocators.ip_ranges_input_field_locator,
                                    campaign_data['platforms_telco_and_devices']['ip_address/ranges'])
        time.sleep(self.TWO_SEC_DELAY)
        # DEVICE
        self.select_from_modal(campaign_data['platforms_telco_and_devices']['device_type'],
                               CampaignFormLocators.device_type_label)
        # OS
        self.select_from_modal(campaign_data['platforms_telco_and_devices']['device_os'],
                               CampaignFormLocators.device_os_label)
        time.sleep(self.TWO_SEC_DELAY)
        # BRAND
        if edit_campaign is False:
            self.click_on_element(CampaignFormLocators.device_brands_section_locator)
            time.sleep(self.TWO_SEC_DELAY)
            self.wait_for_element_to_be_clickable(CampaignFormLocators.device_brands_selection_locator)
        self.wait_for_presence_of_element(CampaignFormLocators.device_brands_selection_locator)
        time.sleep(self.TWO_SEC_DELAY)
        self.click_on_element(CampaignFormLocators.device_brands_selection_locator)
        self.select_from_modal(campaign_data['platforms_telco_and_devices']['device_brand'])
        time.sleep(self.TWO_SEC_DELAY)
        # MODEL
        if edit_campaign is False:
            self.click_on_element(CampaignFormLocators.device_models_section_locator)
            self.wait_for_element_to_be_clickable(CampaignFormLocators.device_models_selection_locator)
        self.click_on_element(CampaignFormLocators.device_models_selection_locator)
        time.sleep(self.TWO_SEC_DELAY)
        self.select_from_modal(campaign_data['platforms_telco_and_devices']['device_model'])
        # BROWSER
        self.select_from_modal(campaign_data['platforms_telco_and_devices']['browser'],
                               CampaignFormLocators.device_browsers_label)
        # DEVICE_COST_RANGES
        self.select_from_modal(campaign_data['platforms_telco_and_devices']['device_cost_range'],
                               CampaignFormLocators.device_cost_ranges_label)

    def provide_advanced_telecom_targeting_info(self, campaign_data, edit_campaign=False, multi_country=False):
        if edit_campaign is False:
            if (self.get_attribute_value(CampaignFormLocators.advance_targeting_selection_locator, "aria-expanded")
                    == "false"):
                self.click_on_element(CampaignFormLocators.advance_targeting_selection_locator)
            # SIM_AMOUNT
            if (self.get_attribute_value(CampaignFormLocators.sim_amount_selection_locator, "aria-expanded")
                    == "false"):
                self.click_on_element(CampaignFormLocators.sim_amount_selection_locator)
        if edit_campaign is True:
            self.check_uncheck_specific_checkbox(CampaignFormLocators.one_sim_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.two_sims_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.three_sims_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.four_sims_checkbox_label, False)
        if (self.get_attribute_value(CampaignFormLocators.sim_amount_selection_locator, "aria-expanded")
                == "false"):
            self.click_on_element(CampaignFormLocators.sim_amount_selection_locator)
        self.check_uncheck_specific_checkbox(campaign_data['platforms_telco_and_devices']['sim_amount'], True)
        # DEVICE_CONNECTION
        if edit_campaign is False:
            if (self.get_attribute_value(CampaignFormLocators.device_connection_selection_locator, "aria-expanded")
                    == "false"):
                self.click_on_element(CampaignFormLocators.device_connection_selection_locator)
        if edit_campaign is True:
            self.check_uncheck_specific_checkbox(CampaignFormLocators.two_g_supporting_devices_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.three_g_supporting_devices_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.four_g_supporting_devices_checkbox_label, False)
        if (self.get_attribute_value(CampaignFormLocators.device_connection_selection_locator, "aria-expanded")
                == "false"):
            self.click_on_element(CampaignFormLocators.device_connection_selection_locator)
        self.check_uncheck_specific_checkbox(campaign_data['platforms_telco_and_devices']['device_connection'], True)
        if edit_campaign is False:
            time.sleep(self.TWO_SEC_DELAY)
            self.click_on_device_and_network_connection_specific_radio_button(campaign_data[
                                                                                  'platforms_telco_and_devices'][
                                                                                  'device_connection'],
                                                                              CampaignFormLocators.only_radio_button_label)
        # NETWORK_CONNECTION
        if edit_campaign is False:
            if (self.get_attribute_value(CampaignFormLocators.network_connection_selection_locator, "aria-expanded")
                    == "false"):
                self.click_on_element(CampaignFormLocators.network_connection_selection_locator)
        if edit_campaign is True:
            self.check_uncheck_specific_checkbox(CampaignFormLocators.two_g_network_connection_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.three_g_network_connection_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.four_g_network_connection_checkbox_label, False)
        if (self.get_attribute_value(CampaignFormLocators.network_connection_selection_locator, "aria-expanded")
                == "false"):
            self.click_on_element(CampaignFormLocators.network_connection_selection_locator)
        self.check_uncheck_specific_checkbox(campaign_data['platforms_telco_and_devices']['network_connection'], True)
        if edit_campaign is False:
            time.sleep(self.TWO_SEC_DELAY)
            self.click_on_device_and_network_connection_specific_radio_button(campaign_data[
                                                                                  'platforms_telco_and_devices'][
                                                                                  'network_connection'],
                                                                              CampaignFormLocators.only_radio_button_label)
        # MULTIPLE_SIM
        if multi_country is False:
            self.select_from_modal(campaign_data['platforms_telco_and_devices']['multiple_operation_sim_card'],
                                   CampaignFormLocators.multiple_operator_sim_card_label)
        else:
            self.select_multiple_item_from_modal(
                campaign_data['platforms_telco_and_devices']['multiple_operation_sim_card'],
                CampaignFormLocators.multiple_operator_sim_card_label)
        # DATA_CONSUMPTION
        self.select_from_modal(campaign_data['platforms_telco_and_devices']['mobile_data_consumption'],
                               CampaignFormLocators.mobile_data_consumption_label)
        # OPERATOR_CHURN
        if multi_country is False:
            self.select_from_modal(campaign_data['platforms_telco_and_devices']['operator_churn'],
                                   CampaignFormLocators.operator_churn_label)
        else:
            self.select_multiple_item_from_modal(campaign_data['platforms_telco_and_devices']['operator_churn'],
                                                 CampaignFormLocators.operator_churn_label)

    def provide_optimizations_deals_packages_info(self, campaign_data, edit_campaign=False, ingame=False, multi_creative=False):
        if edit_campaign is False:
            self.click_on_element(CampaignFormLocators.optimisations_deals_packages_group_locator)
            self.click_on_element(CampaignFormLocators.impression_capping_section_locator)
            # IMPRESSION_CAPPING
            self.check_uncheck_specific_checkbox(CampaignFormLocators.default_impression_capping_checkbox_label, False)
        self.set_value_into_element(CampaignFormLocators.impression_input_field_locator,
                                    campaign_data['optimisations_deals_and_packages']['impression_amount'])
        self.set_value_into_element(CampaignFormLocators.impression_click_input_field_locator,
                                    campaign_data['optimisations_deals_and_packages']['impression_click'])
        self.set_value_into_element(CampaignFormLocators.impression_time_input_field_locator,
                                    campaign_data['optimisations_deals_and_packages']['impression_time'])
        time.sleep(self.TWO_SEC_DELAY)
        # AUTO_OPTIMIZATION
        if edit_campaign is False:
            self.click_on_element(CampaignFormLocators.auto_optimisation_section_locator)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.default_optimisations_settings_checkbox_label,
                                                 False)
            time.sleep(self.TWO_SEC_DELAY)
        if edit_campaign is True:
            self.check_uncheck_specific_checkbox(CampaignFormLocators.cpc_cost_per_click_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.ctr_click_through_rate_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.cpa_cost_per_action_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.vr_viewability_rate_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.er_engagement_rate_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.cpe_cost_per_engagement_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.sr_session_rate_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.cps_cost_per_session_checkbox_label, False)
        self.check_uncheck_specific_checkbox(campaign_data['optimisations_deals_and_packages']['auto_opt_checkbox'],
                                             True)
        # CTR
        time.sleep(self.TWO_SEC_DELAY)
        self.set_value_into_specific_input_field_under_auto_optimisation(
            campaign_data['optimisations_deals_and_packages']['auto_opt_checkbox'],
            campaign_data['optimisations_deals_and_packages']['minimum_ctr'], "", True)
        self.set_value_into_specific_input_field_under_auto_optimisation(
            campaign_data['optimisations_deals_and_packages']['auto_opt_checkbox'],
            campaign_data['optimisations_deals_and_packages']['minimum_imp_per_placement_to_learn'],
            CampaignFormLocators.minimum_impressions_per_placement_to_learn_field_label, )
        self.set_value_into_specific_input_field_under_auto_optimisation(
            campaign_data['optimisations_deals_and_packages']['auto_opt_checkbox'],
            campaign_data['optimisations_deals_and_packages']['minimum_spend_per_placement_to_learn'],
            CampaignFormLocators.minimum_spend_per_placement_to_learn_field_label)
        # AD_EXCHANGE
        if ingame is False:
            if edit_campaign is False:
                self.click_on_element(CampaignFormLocators.ad_exchanges_section_locator)
            self.wait_for_element_to_be_clickable(CampaignFormLocators.ad_exchanges_uncheck_all_button_locator)
            self.click_on_element(CampaignFormLocators.ad_exchanges_uncheck_all_button_locator)
            self.check_uncheck_specific_checkbox(campaign_data['optimisations_deals_and_packages']['ad_exchange_checkbox'],
                                                 True)
        # PLACEMENT_POSITION
        if multi_creative is False:
            if edit_campaign is False:
                self.click_on_element(CampaignFormLocators.ad_placement_positions_section_locator)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.above_the_fold_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.below_the_fold_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.footer_sticky_ad_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.full_screen_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.header_sticky_ad_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.other_checkbox_label, False)
            self.check_uncheck_specific_checkbox(CampaignFormLocators.sidebar_sticky_ad_checkbox_label, False)
            self.check_uncheck_specific_checkbox(
                campaign_data['optimisations_deals_and_packages']['ad_placement_position_checkbox'], True)

    def provide_landing_and_creatives_info(self, campaign_data):
        # CLICK URL
        self.wait_for_presence_of_element(CampaignFormLocators.click_url_input_field_locator)
        self.set_value_into_element(CampaignFormLocators.click_url_input_field_locator,
                                    campaign_data['landing_and_creatives']['click_url'])
        time.sleep(self.TWO_SEC_DELAY)
        # AD DOMAIN
        self.click_on_element(CampaignFormLocators.ad_domain_field_locator)
        self.wait_for_presence_of_element(CampaignFormLocators.tick_or_cross_sign_click_url_locator)
        self.set_value_into_element(CampaignFormLocators.ad_domain_search_field_locator,
                                    campaign_data['landing_and_creatives']['ad_domain'])
        time.sleep(self.TWO_SEC_DELAY)
        self.wait_for_presence_of_element(CampaignFormLocators.ad_domain_search_field_locator).send_keys(Keys.ENTER)
        time.sleep(self.TWO_SEC_DELAY)
        # CREATIVE_SELECTION
        self.select_from_modal(campaign_data['landing_and_creatives']['creative'],
                               CampaignFormLocators.selected_creative_sets_selection_label)

    def click_save_cancel_or_draft(self, action):
        if action.lower() == 'save':
            time.sleep(self.TWO_SEC_DELAY)
            self.click_on_element(CampaignFormLocators.button_group_locator)
            self.wait_for_presence_of_element(CampaignFormLocators.publish_button_locator)
            self.wait_for_element_to_be_clickable(CampaignFormLocators.publish_button_locator)
            time.sleep(self.TWO_SEC_DELAY)
            self.click_on_element(CampaignFormLocators.publish_button_locator)
        elif action.lower() == 'cancel':
            time.sleep(self.TWO_SEC_DELAY)
            self.click_on_element(CampaignFormLocators.button_group_locator)
            self.wait_for_presence_of_element(CampaignFormLocators.cancel_button_locator)
            self.wait_for_element_to_be_clickable(CampaignFormLocators.cancel_button_locator)
            self.click_on_element(CampaignFormLocators.cancel_button_locator)
            time.sleep(self.FIVE_SEC_DELAY)
        elif action.lower() == 'draft':
            time.sleep(self.TWO_SEC_DELAY)
            self.click_on_element(CampaignFormLocators.button_group_locator)
            self.wait_for_presence_of_element(CampaignFormLocators.draft_button_locator)
            self.wait_for_element_to_be_clickable(CampaignFormLocators.draft_button_locator)
            self.click_on_element(CampaignFormLocators.draft_button_locator)
            time.sleep(self.FIVE_SEC_DELAY)

    def provide_campaign_data_and_save(self, campaign_data, action, edit_campaign=False,
                                       duplicate_campaign=False, multi_platform=False, ingame=False, multi_creative=False):
        if duplicate_campaign:
            step_printer("NAME_AND_TYPE")
            self.provide_name_and_type_info(campaign_data, duplicate_or_edit_campaign=True)
            step_printer("LAUNCH_DATE_AND_BUDGET")
            self.provide_launch_date_and_budget_info(campaign_data, duplicate_campaign=True)
            step_printer('SAVE, CANCEL OR DRAFT')
            self.click_save_cancel_or_draft(action)
        else:
            step_printer("NAME_AND_TYPE")
            self.provide_name_and_type_info(campaign_data, edit_campaign, multi_platform, ingame)
            step_printer("LAUNCH_DATE_AND_BUDGET")
            self.provide_launch_date_and_budget_info(campaign_data)
            step_printer("LOCATION_AND_AUDIENCES")
            self.provide_location_and_audiences_info(campaign_data, edit_campaign)
            step_printer("CAMPAIGN_PURPOSE")
            self.provide_campaign_purpose_info(campaign_data, edit_campaign)
            time.sleep(self.TWO_SEC_DELAY)
            step_printer('PLATFORMS_TELCO_AND_DEVICES')
            self.provide_platforms_telco_and_devices_info(campaign_data, edit_campaign)
            step_printer('ADVANCED_TELECOM_TARGETING')
            self.provide_advanced_telecom_targeting_info(campaign_data, edit_campaign)
            step_printer('OPTIMIZATIONS_DEALS_PACKAGES')
            self.provide_optimizations_deals_packages_info(campaign_data, edit_campaign, ingame, multi_creative)
            step_printer('LANDING_AND_CREATIVES')
            self.provide_landing_and_creatives_info(campaign_data)
            step_printer('SAVE, CANCEL OR DRAFT')
            self.click_save_cancel_or_draft(action)

    def get_unavailable_creative_type_alert_message(self):
        time.sleep(self.TWO_SEC_DELAY)
        return self.get_element_text(CampaignFormLocators.unavailable_creative_type_alert_locator)

    def provide_campaign_data_and_save_for_multiple_platform_and_multiple_country(self, campaign_data, action,
                                                                                  multi_platform=False,
                                                                                  multi_country=False):

        step_printer("NAME_AND_TYPE")
        self.provide_name_and_type_info(campaign_data, multi_platform=multi_platform)
        step_printer("LAUNCH_DATE_AND_BUDGET")
        self.provide_launch_date_and_budget_info(campaign_data)
        step_printer("LOCATION_AND_AUDIENCES")
        self.provide_location_and_audiences_info_for_mul_platform_and_country(campaign_data,
                                                                              multi_platform=multi_platform,
                                                                              multi_country=multi_country)
        time.sleep(self.TWO_SEC_DELAY)
        if multi_platform is False:
            step_printer('PLATFORMS_TELCO_AND_DEVICES')
            self.provide_platforms_telco_and_devices_info(campaign_data, multi_country=multi_country)
            step_printer('ADVANCED_TELECOM_TARGETING')
            self.provide_advanced_telecom_targeting_info(campaign_data, multi_country=multi_country)
            step_printer('OPTIMIZATIONS_DEALS_PACKAGES')
            self.provide_optimizations_deals_packages_info(campaign_data)
        step_printer('LANDING_AND_CREATIVES')
        self.provide_landing_and_creatives_info(campaign_data)
        step_printer('SAVE, CANCEL OR DRAFT')
        self.click_save_cancel_or_draft(action)

    def get_campaign_name_and_type(self):
        self.wait_for_visibility_of_element(CampaignFormLocators.creative_type_dropdown_locator)
        time.sleep(self.TWO_SEC_DELAY)
        campaign_information['name_and_type']['platform_type'] = self.get_attribute_value(CampaignFormLocators.platform_type_locator, "title")
        campaign_information['name_and_type']['creative_type'] = self.get_text_using_tag_attribute(self.span_tag,
                                                                                                   self.id_attribute,
                                                                                                   CampaignFormLocators.type_field_id)

        campaign_information['name_and_type']['campaign_type'] = self.get_element_text(CampaignFormLocators.campaign_type_dropdown_locator)
        campaign_information['name_and_type']['campaign_name'] = self.get_text_using_tag_attribute(self.input_tag,
                                                                                                   self.id_attribute,
                                                                                                   CampaignFormLocators.campaign_field_id)

    def get_campaign_launch_date_and_budget(self):
        time.sleep(self.TWO_SEC_DELAY)
        campaign_information['launch_date_and_budget']['bid_cpm'] = self.get_text_using_tag_attribute(self.input_tag,
                                                                                                      self.id_attribute,
                                                                                                      CampaignFormLocators.bid_cpm_field_id)
        campaign_information['launch_date_and_budget']['daily_budget'] = self.get_text_using_tag_attribute(
            self.input_tag, self.id_attribute, CampaignFormLocators.daily_budget_field_id)
        campaign_information['launch_date_and_budget']['total_budget'] = self.get_text_using_tag_attribute(
            self.input_tag, self.id_attribute, CampaignFormLocators.total_budget_field_id)

    def get_campaign_location_and_audiences(self, multi_platform=False):
        time.sleep(self.TWO_SEC_DELAY)
        if multi_platform is True:
            campaign_information['location_and_audiences'][
                'country_name'] = self.get_selected_value_of_modal_from_field(
                field_label=CampaignFormLocators.country_label)
        else:
            campaign_information['location_and_audiences'][
                'country_name'] = self.get_selected_value_of_modal_from_field(
                field_label=CampaignFormLocators.country_label)
            self.click_on_element(CampaignFormLocators.city_section_locator)
            campaign_information['location_and_audiences']['city_name'] = self.get_selected_value_of_modal_from_field(
                select_tag_id_or_class=CampaignFormLocators.city_dropdown_id)
            self.click_on_element(CampaignFormLocators.state_section_locator)
            time.sleep(self.TWO_SEC_DELAY)
            campaign_information['location_and_audiences']['state_name'] = self.get_selected_value_of_modal_from_field(
                select_tag_id_or_class=CampaignFormLocators.state_dropdown_id)
            campaign_information['location_and_audiences']['audience_include'] = self.get_element_text(CampaignFormLocators.audience_include_value_locator)
            campaign_information['location_and_audiences']['audience_exclude'] = self.get_element_text(CampaignFormLocators.audience_exclude_value_locator)
            campaign_information['location_and_audiences']['age'] = self.get_selected_value_of_modal_from_field(
                field_label=CampaignFormLocators.age_label)
            campaign_information['location_and_audiences']['gender'] = self.get_selected_value_of_modal_from_field(
                field_label=CampaignFormLocators.gender_label)
            campaign_information['location_and_audiences']['language'] = self.get_selected_value_of_modal_from_field(
                field_label=CampaignFormLocators.languages_label)
            campaign_information['location_and_audiences']['sec'] = self.get_selected_value_of_modal_from_field(
                field_label=CampaignFormLocators.sec_socio_economic_class_groups_label)

    def get_campaign_purpose(self):
        campaign_information['campaign_purpose']['campaign_purpose'] = self.get_text_using_tag_attribute(self.span_tag,
                                                                                                         self.id_attribute,
                                                                                                         CampaignFormLocators.campaign_purpose_field_id)
        campaign_information['campaign_purpose']['primary_operator'] = self.get_text_using_tag_attribute(self.span_tag,
                                                                                                         self.id_attribute,
                                                                                                         CampaignFormLocators.primary_operator_field_id)

    def get_campaign_platforms_telco_and_devices(self, campaign_data):
        time.sleep(self.TWO_SEC_DELAY)
        debug_mode = "JENKINS_URL" not in os.environ
        campaign_information['platforms_telco_and_devices'][
            'ad_placement_type'] = self.get_selected_checkbox_name_from_a_section(
            section_div_id=CampaignFormLocators.ad_placement_type_section_id)
        campaign_information['platforms_telco_and_devices'][
            'mobile_operator'] = self.get_selected_value_of_modal_from_field(
            field_label=CampaignFormLocators.mobile_operators_isp_label)
        campaign_information['platforms_telco_and_devices'][
            'ip_address/ranges'] = self.get_element_text(CampaignFormLocators.ip_ranges_input_field_locator)
        campaign_information['platforms_telco_and_devices'][
            'device_type'] = self.get_selected_value_of_modal_from_field(
            field_label=CampaignFormLocators.device_type_label)
        campaign_information['platforms_telco_and_devices'][
            'device_os'] = self.get_selected_value_of_modal_from_field(field_label=CampaignFormLocators.device_os_label)
        campaign_information['platforms_telco_and_devices'][
            'device_brand'] = self.get_selected_value_of_modal_from_field(
            field_label=CampaignFormLocators.device_brands_label)
        campaign_information['platforms_telco_and_devices'][
            'device_model'] = self.get_selected_value_of_modal_from_field(
            field_label=CampaignFormLocators.device_models_label)
        campaign_information['platforms_telco_and_devices'][
            'browser'] = self.get_selected_value_of_modal_from_field(
            field_label=CampaignFormLocators.device_browsers_label)
        campaign_information['platforms_telco_and_devices'][
            'device_cost_range'] = self.get_selected_value_of_modal_from_field(
            field_label=CampaignFormLocators.device_cost_ranges_label)
        campaign_information['platforms_telco_and_devices'][
            'sim_amount'] = self.get_selected_checkbox_name_from_a_section(CampaignFormLocators.sim_amount_section_id)
        if not debug_mode:
            campaign_information['platforms_telco_and_devices'][
                'device_connection'] = campaign_data['platforms_telco_and_devices']['device_connection']
            campaign_information['platforms_telco_and_devices'][
                'network_connection'] = campaign_data['platforms_telco_and_devices']['network_connection']
        else:
            campaign_information['platforms_telco_and_devices'][
                'device_connection'] = self.get_selected_checkbox_name_from_a_section(
                CampaignFormLocators.device_connection_section_id)
            campaign_information['platforms_telco_and_devices'][
                'network_connection'] = self.get_selected_checkbox_name_from_a_section(
                CampaignFormLocators.network_connection_section_id)
        campaign_information['platforms_telco_and_devices'][
            'multiple_operation_sim_card'] = self.get_selected_value_of_modal_from_field(
            field_label=CampaignFormLocators.multiple_operator_sim_card_label)
        campaign_information['platforms_telco_and_devices'][
            'mobile_data_consumption'] = self.get_selected_value_of_modal_from_field(
            field_label=CampaignFormLocators.mobile_data_consumption_label)
        campaign_information['platforms_telco_and_devices'][
            'operator_churn'] = self.get_selected_value_of_modal_from_field(
            field_label=CampaignFormLocators.operator_churn_label)

    def get_campaign_optimisations_deals_and_packages(self, campaign_data, is_draft=False, ingame=False):
        time.sleep(self.TWO_SEC_DELAY)
        campaign_information['optimisations_deals_and_packages'][
            'impression_amount'] = self.get_text_using_tag_attribute(self.input_tag, self.class_attribute,
                                                                     CampaignFormLocators.impression_field_class)
        campaign_information['optimisations_deals_and_packages'][
            'impression_click'] = self.get_text_using_tag_attribute(self.input_tag, self.class_attribute,
                                                                     CampaignFormLocators.impression_click_field_class)
        campaign_information['optimisations_deals_and_packages']['impression_time'] = self.get_text_using_tag_attribute(
            self.input_tag, self.class_attribute, CampaignFormLocators.capping_amount_field_class)
        if is_draft is True:
            self.click_on_element(CampaignFormLocators.auto_optimisation_section_locator)
        campaign_information['optimisations_deals_and_packages'][
            'auto_opt_checkbox'] = self.get_selected_checkbox_name_from_a_section(
            CampaignFormLocators.auto_optimisation_section_id)
        campaign_information['optimisations_deals_and_packages'][
            'minimum_ctr'] = self.get_value_from_specific_input_field_under_auto_optimisation(
            campaign_data['optimisations_deals_and_packages']['auto_opt_checkbox'], "", first_field_value=True)
        campaign_information['optimisations_deals_and_packages'][
            'minimum_imp_per_placement_to_learn'] = self.get_value_from_specific_input_field_under_auto_optimisation(
            campaign_data['optimisations_deals_and_packages']['auto_opt_checkbox'],
            CampaignFormLocators.minimum_impressions_per_placement_to_learn_field_label)
        campaign_information['optimisations_deals_and_packages'][
            'minimum_spend_per_placement_to_learn'] = self.get_value_from_specific_input_field_under_auto_optimisation(
            campaign_data['optimisations_deals_and_packages']['auto_opt_checkbox'],
            CampaignFormLocators.minimum_spend_per_placement_to_learn_field_label)
        if ingame is False:
            campaign_information['optimisations_deals_and_packages'][
                'ad_exchange_checkbox'] = self.get_selected_checkbox_name_from_a_section(
                CampaignFormLocators.exchanges_section_id)
        else:
            campaign_information['optimisations_deals_and_packages'][
                'ad_exchange_checkbox'] = self.get_selected_checkbox_name_from_a_section(
                CampaignFormLocators.exchanges_section_id, multiple=True)
        campaign_information['optimisations_deals_and_packages'][
            'ad_placement_position_checkbox'] = self.get_selected_checkbox_name_from_a_section(
            CampaignFormLocators.ad_placement_positions_section_id)

    def get_campaign_landing_and_creatives(self):
        time.sleep(self.TWO_SEC_DELAY)
        campaign_information['landing_and_creatives']['click_url'] = self.get_text_using_tag_attribute(self.input_tag,
                                                                                                       self.id_attribute,
                                                                                                       CampaignFormLocators.click_url_field_id)
        campaign_information['landing_and_creatives']['ad_domain'] = self.get_text_using_tag_attribute(self.span_tag,
                                                                                                       self.id_attribute,
                                                                                                       CampaignFormLocators.ad_domain_field_id)
        campaign_information['landing_and_creatives']['creative'] = self.get_selected_value_of_modal_from_field(
            field_label=CampaignFormLocators.selected_creative_sets_selection_label)

    def get_campaign_information_with_multiple_attempt(self, campaign_data, multi_platform_or_only_mandatory=False, is_draft=False, multi_country = False , ingame= False):
        if self.get_campaign_information(campaign_data, is_draft, multi_platform_or_only_mandatory, multi_country, ingame) is False:
            self.driver.refresh()
            self.get_campaign_information(campaign_data, is_draft, multi_platform_or_only_mandatory, multi_country, ingame)
        return campaign_information

    def get_campaign_information(self, campaign_data, is_draft, multi_platform_or_only_mandatory=False, multi_country = False, ingame= False):
        status = True
        try:
            self.get_campaign_name_and_type()
            self.get_campaign_launch_date_and_budget()
            self.get_campaign_location_and_audiences(multi_platform_or_only_mandatory)
            if multi_platform_or_only_mandatory is False:
                self.get_campaign_platforms_telco_and_devices(campaign_data)
                if multi_country is False:
                    self.get_campaign_purpose()
                self.get_campaign_optimisations_deals_and_packages(campaign_data, is_draft, ingame)
            self.get_campaign_landing_and_creatives()
            time.sleep(self.TWO_SEC_DELAY)
            self.click_on_element(CampaignFormLocators.button_group_locator)
            self.wait_for_presence_of_element(CampaignFormLocators.cancel_button_locator)
            self.wait_for_element_to_be_clickable(CampaignFormLocators.cancel_button_locator)
            time.sleep(self.TWO_SEC_DELAY)
            self.click_on_element(CampaignFormLocators.cancel_button_locator)
        except:
            status = False
        return status

    def click_on_device_and_network_connection_specific_radio_button(self, checkbox_name, radio_button_name):
        locator = (By.XPATH, "//label[normalize-space()='" + checkbox_name + "']/..//following-sibling::div[1]//label["
                                                                             "normalize-space()='" + radio_button_name + "']")
        self.click_on_element(locator)

    def set_value_into_specific_input_field_under_auto_optimisation(self, checkbox_name, text, field_name="",
                                                                    first_field=False):
        if first_field:
            locator = (By.XPATH, "(//label[normalize-space()='" + checkbox_name + "']/..//..//input)[2]")
        else:
            locator = (By.XPATH, "//label[normalize-space()='" + checkbox_name + "']/..//..//label[normalize-space("
                                                                                 ")='" + field_name + "']/..//input")
        self.set_value_into_element(locator, text)

    def get_value_from_specific_input_field_under_auto_optimisation(self, checkbox_name, field_name="",
                                                                    first_field_value=False):
        if first_field_value:
            locator = (By.XPATH, "(//label[normalize-space()='" + checkbox_name + "']/..//..//input)[2]")
        else:
            locator = (By.XPATH, "//label[normalize-space()='" + checkbox_name + "']/..//..//label[normalize-space("
                                                                                 ")='" + field_name + "']/..//input")
        return self.get_element_text(locator, input_tag=True)
