import time

from pages.base_page import BasePage
from locators.campaign.campaign_approve_form_locator import CampaignApproveLocators

campaign_approve_information = {}


class DspDashboardCampaignApprove(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def provide_main_settings_info(self, main_settings_data):
        # INSERTION ORDER
        self.select_dropdown_value(CampaignApproveLocators.insertion_order_label,
                                   dropdown_item=main_settings_data['io'])
        # ADVERTISER NAME
        self.select_dropdown_value(CampaignApproveLocators.advertiser_name_label,
                                   dropdown_item=main_settings_data['advertiser_name'])
        # ADVERTISEMENT CATEGORY
        self.select_dropdown_value(CampaignApproveLocators.advertiser_category_label,
                                   dropdown_item=main_settings_data['advertisement_category'])
        # APP/SITE CATEGORY
        self.deselect_all_dropdown_value(CampaignApproveLocators.app_site_category_label)
        self.select_dropdown_value(CampaignApproveLocators.app_site_category_label, select_by_value=True,
                                   value=main_settings_data['app_site_category_value'])
        # BRAND SAFETY
        self.select_dropdown_value(CampaignApproveLocators.brand_safety_label,
                                   dropdown_item=main_settings_data['brand_safety'])

    def provide_reporting_and_budget_info(self, reporting_and_budget_data):
        # EMAIL REPORT
        self.check_uncheck_specific_checkbox(CampaignApproveLocators.email_report_label,
                                             bool(reporting_and_budget_data['email_report']['is_checked']))
        self.select_dropdown_value(CampaignApproveLocators.email_report_frequency_label,
                                   dropdown_item=reporting_and_budget_data['email_report']['report_frequency'])
        self.select_dropdown_value(CampaignApproveLocators.email_report_hour_label,
                                   dropdown_item=reporting_and_budget_data['email_report']['report_hour'])
        self.select_dropdown_value(CampaignApproveLocators.email_report_day_label,
                                   dropdown_item=reporting_and_budget_data['email_report']['report_day'])
        # GROUP BY IO
        self.check_uncheck_specific_checkbox(CampaignApproveLocators.group_by_io_label,
                                             bool(reporting_and_budget_data['group_by_io']['is_checked']))
        self.click_on_element(CampaignApproveLocators.button_alert_ok_locator)
        self.select_dropdown_value(CampaignApproveLocators.group_by_io_label,
                                   dropdown_item=reporting_and_budget_data['group_by_io']['view_by'])
        # EMAIL ATTACHMENT
        self.check_uncheck_specific_checkbox(CampaignApproveLocators.email_attachments_label,
                                             bool(reporting_and_budget_data['email_attachment']['xls']['is_checked']),
                                             value="xls")
        self.check_uncheck_specific_checkbox(CampaignApproveLocators.email_attachments_label,
                                             bool(reporting_and_budget_data['email_attachment']['pdf']['is_checked']),
                                             value="pdf")
        # GENERATE INSIGHT REPORT
        self.select_dropdown_value(CampaignApproveLocators.generate_insight_report_label,
                                   dropdown_item=reporting_and_budget_data['generate_insight_report'])
        # TECH FEE
        self.set_value_into_element(CampaignApproveLocators.tech_fee_locator, reporting_and_budget_data['tech_fee'])
        # BUDGET PACING
        self.select_dropdown_value(CampaignApproveLocators.budget_pacing_label,
                                   dropdown_item=reporting_and_budget_data['budget_pacing'])
        # DAILY BUDGET RECALCULATION
        self.check_uncheck_specific_checkbox(CampaignApproveLocators.daily_budget_recalculation_label,
                                             bool(reporting_and_budget_data['daily_budget_recalculation']))

    def provide_optimisation_and_tracking_info(self, optimization_and_tracking_data):
        # IMPRESSION PERFORMANCE METRIC
        self.click_on_element(CampaignApproveLocators.impression_performance_metric_locator)
        self.set_value_into_element(CampaignApproveLocators.impression_performance_metric_viewability_locator,
                                    optimization_and_tracking_data['impression_performance_metric']['viewability'])
        self.set_value_into_element(CampaignApproveLocators.impression_performance_metric_ctr,
                                    optimization_and_tracking_data['impression_performance_metric']['ctr'])
        self.set_value_into_element(CampaignApproveLocators.impression_performance_metric_vcr,
                                    optimization_and_tracking_data['impression_performance_metric']['vcr'])
        # CUSTOM IMPRESSION TRACKING
        self.click_on_element(CampaignApproveLocators.custom_impression_tracking_locator)
        self.select_dropdown_value_from_div(self.id_attribute,
                                            CampaignApproveLocators.custom_impression_tracking_dropdown_id,
                                            dropdown_item=optimization_and_tracking_data['custom_impression_tracking'][
                                                'option'])
        self.click_on_element(CampaignApproveLocators.add_more_custom_impression_tracking_locator)
        self.set_value_into_element(CampaignApproveLocators.custom_impression_tracking_textarea_locator,
                                    optimization_and_tracking_data['custom_impression_tracking']['value'])
        # VIEWABILITY AND VIDEO SUPPORT
        self.click_on_element(CampaignApproveLocators.viewability_and_video_support_locator)
        self.check_uncheck_specific_checkbox(optimization_and_tracking_data['viewability_and_video_support'], True)
        # VIDEO PLAYER REQUIREMENTS
        self.click_on_element(CampaignApproveLocators.video_player_requirement_locator)
        self.check_uncheck_specific_checkbox(optimization_and_tracking_data['vide_player_requirement'], True)
        # MRAID SUPPORT
        self.click_on_element(CampaignApproveLocators.mraid_support_locator)
        self.check_uncheck_specific_checkbox(optimization_and_tracking_data['mraid_support'], True)
        # STRICT CREATIVE SIZE PLACEMENT
        self.check_uncheck_specific_checkbox(CampaignApproveLocators.strict_size_placement_label,
                                             bool(optimization_and_tracking_data['strict_size_placement_size']))
        # MULTIPLE BID PER SECOND
        self.check_uncheck_specific_checkbox(CampaignApproveLocators.multiple_bid_per_second_label,
                                             bool(optimization_and_tracking_data['multiple_bids_per_second']))
        # ENHANCED REACH METRICS
        self.set_value_into_element(CampaignApproveLocators.enhanced_min_reach_locator,
                                    optimization_and_tracking_data['enhanced_reach_metric']['min'])
        self.set_value_into_element(CampaignApproveLocators.enhanced_max_reach_locator,
                                    optimization_and_tracking_data['enhanced_reach_metric']['max'])
        # CAMPAIGN ALSO RUNS ON ESKIMI
        self.check_uncheck_specific_checkbox(CampaignApproveLocators.campaign_also_run_on_eskimi_label, bool(
            optimization_and_tracking_data['campaign_run_on_eskimi']['is_checked']))
        time.sleep(self.TWO_SEC_DELAY)
        self.set_value_into_element(CampaignApproveLocators.campaign_also_run_eskimi_text_locator,
                                    optimization_and_tracking_data['campaign_run_on_eskimi']['value'])

    def provide_ad_exchange_info(self, ad_exchange_data):
        # AD EXCHANGE
        self.check_uncheck_specific_checkbox(CampaignApproveLocators.margin_type_label, True,
                                             value=ad_exchange_data['margin_type_value'])
        self.check_uncheck_specific_checkbox(CampaignApproveLocators.ad_exchange_margin_label,
                                             bool(ad_exchange_data['eskimi_margin']), without_text=True)
        self.set_value_into_element(
            CampaignApproveLocators.ad_exchange_margin_text_xpath.format(
                CampaignApproveLocators.ad_exchange_margin_label),
            ad_exchange_data['eskimi_margin_value'], locator_initialization=True)

    def click_approve_button(self):
        self.click_on_element(CampaignApproveLocators.approve_button_locator)

    def approve_campaign(self, campaign_approve_data):
        self.provide_main_settings_info(campaign_approve_data['main_settings'])
        self.provide_reporting_and_budget_info(campaign_approve_data['reporting_and_budget'])
        self.provide_optimisation_and_tracking_info(campaign_approve_data['optimization_and_tracking'])
        self.provide_ad_exchange_info(campaign_approve_data['ad_exchange'])
        self.click_approve_button()

    def get_main_setting_data(self, mass_approve=False):
        # INSERTION ORDER
        campaign_approve_information['main_settings']['io'] = self.get_text_using_tag_attribute(self.span_tag,
                                                                                                self.id_attribute,
                                                                                                CampaignApproveLocators.io_id)
        # ADVERTISER NAME
        campaign_approve_information['main_settings']['advertiser_name'] = self.get_text_using_tag_attribute(
            self.span_tag, self.id_attribute, CampaignApproveLocators.advertiser_name_id)
        # ADVERTISEMENT CATEGORY
        campaign_approve_information['main_settings'][
            'advertisement_category'] = self.get_text_or_value_from_selected_option(
            CampaignApproveLocators.advertiser_category_label)
        if campaign_approve_information['main_settings']['advertisement_category'] == "":
            campaign_approve_information['main_settings']['advertisement_category'] = "IAB19 Technology & Computing"
        # APP/SITE CATEGORY
        campaign_approve_information['main_settings'][
            'app_site_category_value'] = self.get_text_or_value_from_selected_option(
            CampaignApproveLocators.app_site_category_label, value=True)
        # BRAND SAFETY
        if not mass_approve:
            campaign_approve_information['main_settings']['brand_safety'] = self.get_text_or_value_from_selected_option(
                CampaignApproveLocators.brand_safety_label)

    def get_reporting_and_budget_data(self, mass_approve=False):
        if not mass_approve:
            # EMAIL REPORT
            campaign_approve_information['reporting_and_budget']['email_report'][
                'is_checked'] = self.get_checkbox_status(CampaignApproveLocators.email_report_label)
            campaign_approve_information['reporting_and_budget']['email_report'][
                'report_frequency'] = self.get_text_or_value_from_selected_option(
                CampaignApproveLocators.email_report_frequency_label)
            campaign_approve_information['reporting_and_budget']['email_report'][
                'report_hour'] = self.get_text_or_value_from_selected_option(
                CampaignApproveLocators.email_report_hour_label)
            campaign_approve_information['reporting_and_budget']['email_report'][
                'report_day'] = self.get_text_or_value_from_selected_option(
                CampaignApproveLocators.email_report_day_label)
            # GROUP BY IO
            campaign_approve_information['reporting_and_budget']['group_by_io'][
                'is_checked'] = self.get_checkbox_status(CampaignApproveLocators.group_by_io_label)
            campaign_approve_information['reporting_and_budget']['group_by_io'][
                'view_by'] = self.get_text_or_value_from_selected_option(CampaignApproveLocators.group_by_io_label)
            # EMAIL ATTACHMENT
            campaign_approve_information['reporting_and_budget']['email_attachment']['xls'][
                'is_checked'] = self.get_checkbox_status(CampaignApproveLocators.email_attachments_label, value="xls")
            campaign_approve_information['reporting_and_budget']['email_attachment']['pdf'][
                'is_checked'] = self.get_checkbox_status(CampaignApproveLocators.email_attachments_label, value="pdf")
            # GENERATE INSIGHT REPORT
            campaign_approve_information['reporting_and_budget'][
                'generate_insight_report'] = self.get_text_or_value_from_selected_option(
                CampaignApproveLocators.generate_insight_report_label)
        # TECH FEE
        campaign_approve_information['reporting_and_budget']['tech_fee'] = self.get_element_text(
            CampaignApproveLocators.tech_fee_locator, input_tag=True)
        # BUDGET PACING
        campaign_approve_information['reporting_and_budget'][
            'budget_pacing'] = self.get_text_or_value_from_selected_option(CampaignApproveLocators.budget_pacing_label)
        # DAILY BUDGET RECALCULATION
        campaign_approve_information['reporting_and_budget'][
            'daily_budget_recalculation'] = self.get_checkbox_status(
            CampaignApproveLocators.daily_budget_recalculation_label)
        if mass_approve:
            del campaign_approve_information['reporting_and_budget']['email_report']
            del campaign_approve_information['reporting_and_budget']['group_by_io']
            del campaign_approve_information['reporting_and_budget']['email_attachment']['xls']
            del campaign_approve_information['reporting_and_budget']['email_attachment']['pdf']
            del campaign_approve_information['reporting_and_budget']['email_attachment']

    def get_optimisation_and_tracking_data(self, mass_approve=False):
        if not mass_approve:
            # IMPRESSION PERFORMANCE METRIC
            campaign_approve_information['optimization_and_tracking']['impression_performance_metric'][
                'viewability'] = self.get_element_text(
                CampaignApproveLocators.impression_performance_metric_viewability_locator, input_tag=True)
            campaign_approve_information['optimization_and_tracking']['impression_performance_metric'][
                'ctr'] = self.get_element_text(CampaignApproveLocators.impression_performance_metric_ctr,
                                               input_tag=True)
            campaign_approve_information['optimization_and_tracking']['impression_performance_metric'][
                'vcr'] = self.get_element_text(CampaignApproveLocators.impression_performance_metric_vcr,
                                               input_tag=True)
            # CUSTOM IMPRESSION TRACKING
            campaign_approve_information['optimization_and_tracking']['custom_impression_tracking'][
                'option'] = self.get_element_text(CampaignApproveLocators.custom_impression_tracking_dropdown_xpath,
                                                  locator_initialization=True)
            campaign_approve_information['optimization_and_tracking']['custom_impression_tracking'][
                'value'] = self.get_element_text(CampaignApproveLocators.custom_impression_tracking_text_xpath,
                                                 locator_initialization=True)
            # VIEWABILITY AND VIDEO SUPPORT
            campaign_approve_information['optimization_and_tracking'][
                'viewability_and_video_support'] = self.get_selected_checkbox_name_from_a_section(
                CampaignApproveLocators.viewability_and_video_support_div_id, label_is_parent=True)
            # VIDEO PLAYER REQUIREMENTS
            campaign_approve_information['optimization_and_tracking'][
                'vide_player_requirement'] = self.get_selected_checkbox_name_from_a_section(
                CampaignApproveLocators.video_player_requirement_div_id, label_is_parent=True)
            # MRAID SUPPORT
            campaign_approve_information['optimization_and_tracking'][
                'mraid_support'] = self.get_selected_checkbox_name_from_a_section(
                CampaignApproveLocators.mraid_support_div_id, label_is_parent=True)
            # ANTI FRAUD SETTINGS
            campaign_approve_information['optimization_and_tracking'][
                'anti_fraud_setting'] = self.get_selected_checkbox_name_from_a_section(
                CampaignApproveLocators.anti_fraud_setting_div_id, label_is_parent=True, multiple=True)
            # ENHANCED REACH METRICS
            campaign_approve_information['optimization_and_tracking'][
                'enhanced_reach_metric']['min'] = self.get_element_text(
                CampaignApproveLocators.enhanced_min_reach_locator, input_tag=True)
            campaign_approve_information['optimization_and_tracking'][
                'enhanced_reach_metric']['max'] = self.get_element_text(
                CampaignApproveLocators.enhanced_max_reach_locator, input_tag=True)
            # CAMPAIGN ALSO RUNS ON ESKIMI
            campaign_approve_information['optimization_and_tracking'][
                'campaign_run_on_eskimi']['is_checked'] = self.get_checkbox_status(
                CampaignApproveLocators.campaign_also_run_on_eskimi_label)
            campaign_approve_information['optimization_and_tracking'][
                'campaign_run_on_eskimi']['value'] = self.get_element_text(
                CampaignApproveLocators.campaign_also_run_eskimi_text_locator, input_tag=True)
        # STRICT CREATIVE SIZE PLACEMENT
        campaign_approve_information['optimization_and_tracking'][
            'strict_size_placement_size'] = self.get_checkbox_status(
            CampaignApproveLocators.strict_size_placement_label)
        # MULTIPLE BID PER SECOND
        campaign_approve_information['optimization_and_tracking'][
            'multiple_bids_per_second'] = self.get_checkbox_status(
            CampaignApproveLocators.multiple_bid_per_second_label)
        if mass_approve:
            del campaign_approve_information['optimization_and_tracking']['impression_performance_metric']
            del campaign_approve_information['optimization_and_tracking']['custom_impression_tracking']
            del campaign_approve_information['optimization_and_tracking']['enhanced_reach_metric']
            del campaign_approve_information['optimization_and_tracking']['campaign_run_on_eskimi']

    def get_ad_exchange_data(self):
        # AD EXCHANGE
        campaign_approve_information['ad_exchange']['margin_type_value'] = self.get_checked_element_value_attribute(
            CampaignApproveLocators.margin_type_label)
        campaign_approve_information['ad_exchange']['eskimi_margin'] = self.get_checkbox_status(
            CampaignApproveLocators.ad_exchange_margin_label, without_text=True)
        campaign_approve_information['ad_exchange']['eskimi_margin_value'] = self.get_element_text(
            CampaignApproveLocators.ad_exchange_margin_text_xpath.format(
                CampaignApproveLocators.ad_exchange_margin_label),
            input_tag=True, locator_initialization=True)

    @staticmethod
    def reset_campaign_approve_information():
        # RESET CAMPAIGN APPROVE INFORMATION BEFORE GETTING DATA
        global campaign_approve_information
        campaign_approve_information = {'main_settings': {},
                                        'reporting_and_budget': {'email_report': {}, 'group_by_io': {},
                                                                 'email_attachment': {'xls': {}, 'pdf': {}}},
                                        'optimization_and_tracking': {'impression_performance_metric': {},
                                                                      'custom_impression_tracking': {},
                                                                      'enhanced_reach_metric': {},
                                                                      'campaign_run_on_eskimi': {}},
                                        'ad_exchange': {}}

    def get_campaign_approve_data(self, mass_approve=False):
        self.reset_campaign_approve_information()
        self.get_main_setting_data(mass_approve)
        self.get_reporting_and_budget_data(mass_approve)
        self.get_optimisation_and_tracking_data(mass_approve)
        self.get_ad_exchange_data()
        return campaign_approve_information

    def get_campaign_status(self):
        return self.get_element_text(CampaignApproveLocators.campaign_status_label_locator)

    def click_delete_button(self):
        self.click_on_element(CampaignApproveLocators.delete_button_locator)
        self.wait_alert_is_present()
        self.accept_alert()
