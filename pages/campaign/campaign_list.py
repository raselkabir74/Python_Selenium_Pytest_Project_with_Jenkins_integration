from locators.campaign.campaign_list_locator import CampaignListLocators
from pages.base_page import BasePage
from configurations import generic_modules
import time


class DspDashboardCampaignsList(BasePage):

    def __init__(self, driver):
        super().__init__(driver)
        self.driver = driver

    def reload_campaign_list_page(self):
        self.driver.get(generic_modules.BASE_URL)
        self.wait_for_element_to_be_clickable(CampaignListLocators.campaign_search_field_locator)

    def select_all_status(self):
        status_selected = self.get_text_using_tag_attribute(self.span_tag, self.id_attribute,
                                                            CampaignListLocators.status_dropdown_id)
        if status_selected != "All":
            self.click_on_element(CampaignListLocators.status_dropdown_locator)
            self.click_on_element(CampaignListLocators.all_status_option_locator)
            time.sleep(self.TWO_SEC_DELAY)

    def navigate_to_add_campaign_group(self):
        self.click_on_element(CampaignListLocators.btn_create_locator)

    def get_draft_status_text(self):
        return self.get_element_text(CampaignListLocators.campaign_list_draft_status)

    def get_success_message(self):
        return self.get_element_text(CampaignListLocators.success_message_locator)

    def search_and_action(self, campaign_name, action="None", force_reload=False):
        try:
            if force_reload:
                self.reload_campaign_list_page()
                self.set_value_into_element(CampaignListLocators.campaign_search_field_locator, campaign_name)
            else:
                self.set_value_into_element(CampaignListLocators.campaign_search_field_locator, campaign_name)
        except Exception:
            self.reload_campaign_list_page()
            self.set_value_into_element(CampaignListLocators.campaign_search_field_locator, campaign_name)
        self.wait_for_visibility_of_element(CampaignListLocators.three_dot_of_campaign_xpath.format(campaign_name),
                                            locator_initialization=True)
        if action != 'None':
            self.click_element_execute_script(CampaignListLocators.three_dot_of_campaign_xpath.format(campaign_name))
        if action.lower() == 'edit':
            time.sleep(self.TWO_SEC_DELAY)
            self.click_element_execute_script(CampaignListLocators.campaign_list_edit_locator)
        elif action.lower() == 'delete':
            self.click_element_execute_script(CampaignListLocators.campaign_list_delete_locator)
            self.click_on_element(CampaignListLocators.confirm_button_alert_locator)
        elif action.lower() == 'approve':
            self.click_element_execute_script(CampaignListLocators.campaign_list_approve_locator)
        elif action.lower() == 'duplicate':
            self.click_element_execute_script(CampaignListLocators.three_dot_of_campaign_xpath.format(campaign_name))
            self.click_element_execute_script(CampaignListLocators.campaign_list_duplicate_locator)
        elif action.lower() == 'campaign goals':
            self.click_on_three_dot_option(CampaignListLocators.campaign_goals_label, CampaignListLocators.campaign_table_id)

    def check_uncheck_campaign_list_grid_row_checkbox(self, campaign_name="", check_the_checkbox=False,
                                                      check_all_checkbox=False):
        self.check_uncheck_specific_grid_row_checkbox(CampaignListLocators.campaign_table_id,
                                                      check_all_checkbox=check_all_checkbox,
                                                      check_the_checkbox=check_the_checkbox,
                                                      column_value_to_identify_column=campaign_name)
        time.sleep(self.TWO_SEC_DELAY)

    def select_item_from_campaign_multi_action_menu(self, item_name_to_select, switch_to_new_window=False):
        self.select_item_from_multi_action_menu(CampaignListLocators.campaign_multi_actions_menu_id,
                                                item_name_to_select)
        time.sleep(self.TWO_SEC_DELAY)
        if item_name_to_select == "Delete":
            self.click_on_element(CampaignListLocators.confirm_button_alert_locator)
        if switch_to_new_window:
            self.switch_to_new_window()
