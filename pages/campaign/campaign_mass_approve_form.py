from locators.campaign.campaign_mass_approve_form_locators import CampaignMassApproveFormLocators
from pages.base_page import BasePage


class DspDashboardCampaignsMassApprove(BasePage):

    def __init__(self, driver):
        super().__init__(driver)

    def provide_campaign_mass_approve_data_and_save(self, campaign_name_list, mass_approve_campaign_data):
        self.wait_for_visibility_of_element(CampaignMassApproveFormLocators.mass_approve_header_locator)
        for iteration in range(len(campaign_name_list)):
            # INSERTION ORDER
            self.select_dropdown_value_from_specific_form_grid(
                CampaignMassApproveFormLocators.campaign_mass_approve_form_id,
                CampaignMassApproveFormLocators.insertion_order_column,
                mass_approve_campaign_data['main_settings']['io'], str(iteration + 2), search_option_available=False)
            # ADVERTISER NAME
            self.select_dropdown_value_from_specific_form_grid(
                CampaignMassApproveFormLocators.campaign_mass_approve_form_id,
                CampaignMassApproveFormLocators.advertiser_name_column,
                mass_approve_campaign_data['main_settings']['advertiser_name'], str(iteration + 2))
            # ADVERTISEMENT CATEGORY
            self.click_link_of_specific_column_of_specific_row_from_grid(
                CampaignMassApproveFormLocators.campaign_mass_approve_form_id,
                CampaignMassApproveFormLocators.advertisement_category_column, str(iteration + 2))
            self.dropdown_selection(
                CampaignMassApproveFormLocators.advertisement_category_modal_xpath.format(str(iteration)),
                dropdown_item=mass_approve_campaign_data['main_settings']['advertisement_category'])
            self.click_ok_button_of_specific_column_modal_from_grid(
                CampaignMassApproveFormLocators.campaign_mass_approve_form_id,
                CampaignMassApproveFormLocators.advertisement_category_column, str(iteration + 2))
            # APP/SITE CATEGORY
            self.click_link_of_specific_column_of_specific_row_from_grid(
                CampaignMassApproveFormLocators.campaign_mass_approve_form_id,
                CampaignMassApproveFormLocators.app_site_category_column, str(iteration + 2))
            self.deselect_all_options_from_grid_modal(
                CampaignMassApproveFormLocators.app_site_category_modal_xpath.format(str(iteration)))
            self.dropdown_selection(
                CampaignMassApproveFormLocators.app_site_category_modal_xpath.format(str(iteration)),
                select_by_value=True,
                value=mass_approve_campaign_data['main_settings']['app_site_category_value'])
            self.click_ok_button_of_specific_column_modal_from_grid(
                CampaignMassApproveFormLocators.campaign_mass_approve_form_id,
                CampaignMassApproveFormLocators.app_site_category_column, str(iteration + 2))
            # BUDGET PACING
            self.select_dropdown_value_from_specific_form_grid(
                CampaignMassApproveFormLocators.campaign_mass_approve_form_id,
                CampaignMassApproveFormLocators.budget_pacing_column,
                mass_approve_campaign_data['reporting_and_budget']['budget_pacing'], str(iteration + 2),
                search_option_available=False)
            # DAILY BUDGET RECALCULATION
            self.check_uncheck_specific_form_grid_row_checkbox(
                CampaignMassApproveFormLocators.campaign_mass_approve_form_id,
                CampaignMassApproveFormLocators.daily_budget_recalculation_column,
                bool(mass_approve_campaign_data['reporting_and_budget']['daily_budget_recalculation']),
                str(iteration + 2))
            # STRICT PLACEMENT SIZE
            self.check_uncheck_specific_form_grid_row_checkbox(
                CampaignMassApproveFormLocators.campaign_mass_approve_form_id,
                CampaignMassApproveFormLocators.strict_creative_size_placement_column,
                bool(mass_approve_campaign_data['optimization_and_tracking']['strict_size_placement_size']),
                str(iteration + 2))
            # MULTIPLE BIDS PER SECOND
            self.check_uncheck_specific_form_grid_row_checkbox(
                CampaignMassApproveFormLocators.campaign_mass_approve_form_id,
                CampaignMassApproveFormLocators.multiple_bids_per_user_second_column,
                bool(mass_approve_campaign_data['optimization_and_tracking']['multiple_bids_per_second']),
                str(iteration + 2))
            # AD EXCHANGE
            self.click_link_of_specific_column_of_specific_row_from_grid(
                CampaignMassApproveFormLocators.campaign_mass_approve_form_id,
                CampaignMassApproveFormLocators.ad_exchange_column, str(iteration + 2))
            self.check_uncheck_specific_form_grid_row_checkbox_modal(CampaignMassApproveFormLocators.margin_type_label,
                                                                     True,
                                                                     value=mass_approve_campaign_data['ad_exchange'][
                                                                         'margin_type_value'],
                                                                     row_number=str(iteration + 2))
            self.check_uncheck_specific_form_grid_row_checkbox_modal(
                CampaignMassApproveFormLocators.ad_exchange_name_label,
                bool(mass_approve_campaign_data['ad_exchange']['eskimi_margin']),
                row_number=str(iteration + 2))
            ad_exchange_margin_text_locator = CampaignMassApproveFormLocators.ad_exchange_text_field_xpath.format(
                CampaignMassApproveFormLocators.ad_exchange_name_label, str(iteration + 2))
            self.set_value_into_element(ad_exchange_margin_text_locator,
                                        mass_approve_campaign_data['ad_exchange']['eskimi_margin_value'],
                                        locator_initialization=True)
            self.click_ok_button_of_specific_column_modal_from_grid(
                CampaignMassApproveFormLocators.campaign_mass_approve_form_id,
                CampaignMassApproveFormLocators.ad_exchange_column, str(iteration + 2))
        self.click_on_element(CampaignMassApproveFormLocators.approve_button_locator)
