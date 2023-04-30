import time

from selenium.webdriver.common.by import By
from pages.base_page import BasePage


class DspDashboardOptimization(BasePage):
    def __init__(self, config, driver):
        super().__init__(driver)
        self.config = config
        self.driver = driver

    def click_on_play_pause_button(self, row_number, optimisation_type, is_play=False, group_action=False,
                                   single_action=False,
                                   bulk_action=False):
        td = self.get_optimisation_wise_column_number(optimisation_type)
        if is_play:
            group_action_play_pause_button_locator = (By.XPATH, "//table[@id='optimization_table']//tbody//tr[" +
                                                      row_number + "]//td[" + str(td) + "]//i[contains(@class, "
                                                                                        "'play')]")
            single_action_play_pause_button_locator = (By.XPATH, "//table[@id='optimization_table']//tbody//tr[" +
                                                       row_number + "]//td[" + str(td - 1) + "]//i[contains(@class, "
                                                                                             "'play')]")
            bulk_action_play_pause_button_locator = (
                By.XPATH, "(//a[@id='action-all-optimize-by-start']//i)[2]")
        else:
            group_action_play_pause_button_locator = (
                By.XPATH,
                "//table[@id='optimization_table']//tbody//tr[" + row_number + "]//td[" + str(td) + "]//i[contains("
                                                                                                    "@class, 'pause')]")
            single_action_play_pause_button_locator = (
                By.XPATH, "//table[@id='optimization_table']//tbody//tr[" + row_number + "]//td[" + str(td - 1) +
                "]//i[contains(@class, 'pause')]")
            bulk_action_play_pause_button_locator = (By.XPATH, "(//a[@id='action-all-optimize-by-stop']//i)[2]")
        if group_action:
            self.click_element_execute_script(group_action_play_pause_button_locator, locator_initialize= True)
            time.sleep(self.TWO_SEC_DELAY)
        elif single_action:
            if self.is_element_present(single_action_play_pause_button_locator, 2):
                elements = self.wait_for_presence_of_all_elements_located(single_action_play_pause_button_locator)
                for iteration in range(len(elements)):
                    self.click_element_execute_script(single_action_play_pause_button_locator, locator_initialize= True)
                time.sleep(self.TWO_SEC_DELAY)
        elif bulk_action:
            self.click_element_execute_script(bulk_action_play_pause_button_locator, locator_initialize= True)
            time.sleep(self.FIVE_SEC_DELAY)

    def select_specific_date_range_for_optimisation(self, date_range_to_select):
        field_locator = (By.ID, "date-range")
        date_range_locator = (By.XPATH, "//a[contains(text(), '" + date_range_to_select + "')]")
        self.click_on_element(field_locator)
        self.click_on_element(date_range_locator)

    def get_specific_play_pause_button_status(self, row_number, optimisation_type, expected_status,
                                              group_and_single_action=False, bulk_action=False):
        td = self.get_optimisation_wise_column_number(optimisation_type)
        status = True
        if group_and_single_action:
            time.sleep(self.TWO_SEC_DELAY)
            single_action_play_pause_button_locator = (
                By.XPATH, "//table[@id='optimization_table']//tbody//tr[" + row_number + "]//td[" + str(td - 1) +
                "]//i")
            elements = self.wait_for_presence_of_all_elements_located(single_action_play_pause_button_locator)
            for iteration in range(len(elements)):
                single_play_pause_button_locator = (
                    By.XPATH, "(//table[@id='optimization_table']//tbody//tr[" + row_number + "]//td[" + str(td - 1) +
                    "]//i)[""" + str(iteration + 1) + "]")
                if not (expected_status in self.get_attribute_value(single_play_pause_button_locator, "class")):
                    status = False
                    break
        elif bulk_action:
            time.sleep(self.FIVE_SEC_DELAY)
            total_row_locator = (By.XPATH, "//table[@id='optimization_table']//tbody//tr")
            total_rows = self.wait_for_presence_of_all_elements_located(total_row_locator)
            if len(total_rows) > 10:
                total_rows = 10
            for iteration in range(len(total_rows)):
                if not status:
                    break
                single_action_play_pause_button_locator = (
                    By.XPATH, "//table[@id='optimization_table']//tbody//tr[" + str(iteration + 1) + "]//td[" + str(
                        td - 1) + "]//i")
                if self.is_element_present(single_action_play_pause_button_locator, self.ONE_SEC_DELAY):
                    elements = self.wait_for_presence_of_all_elements_located(single_action_play_pause_button_locator)
                    for index in range(len(elements)):
                        single_play_pause_button_locator = (
                            By.XPATH, "(//table[@id='optimization_table']//tbody//tr[" + str(
                                iteration + 1) + "]//td[" + str(td - 1) + "]//i)[""" + str(index + 1) + "]")
                        if self.is_element_present(single_play_pause_button_locator, self.ONE_SEC_DELAY):
                            if not (expected_status in self.get_attribute_value(single_play_pause_button_locator, "class")):
                                status = False
                                break
        return status

    def get_optimisation_wise_column_number(self, optimisation_type):
        td = 22
        if optimisation_type.lower() == "creative" or optimisation_type.lower() == "app_site_name":
            td = 23
        elif optimisation_type.lower() == "package":
            td = 25
        return td
