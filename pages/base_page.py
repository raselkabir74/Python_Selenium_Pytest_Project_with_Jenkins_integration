import time
import datetime as dt

from selenium.webdriver import ActionChains
from selenium.webdriver.support.select import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from datetime import datetime, date
from configurations import generic_modules
from selenium.webdriver.common.alert import Alert

""" This class is the parent of all pages """
""" It contains all the generic methods and functionalities available to all the pages """


class BasePage:
    ONE_MINUTE = generic_modules.ONE_MINUTE_DELAY
    HALF_MINUTE = generic_modules.HALF_MINUTE_DELAY
    TWO_SEC_DELAY = generic_modules.SHORT_DELAY
    FIVE_SEC_DELAY = generic_modules.FIVE_SEC_DELAY
    ONE_SEC_DELAY = generic_modules.ONE_SEC_DELAY

    # [Start] Tag Names
    input_tag = "input"
    a_tag = "a"
    div_tag = "div"
    span_tag = "span"
    textarea_tag = "textarea"
    li_tag = "li"
    td_tag = "td"
    # [End] Tag Names

    # [Start] Attribute Names
    class_attribute = "class"
    id_attribute = "id"
    title_attribute = "title"
    name_attribute = "name"

    # [End] Attribute Names

    def __init__(self, driver):
        self.driver = driver

    def click_on_sidebar_menu(self, menu_name):
        locator = By.XPATH, "//*[@data-original-title='" + menu_name + "']//i"
        self.wait_for_element_to_be_clickable(locator).click()

    def click_on_element(self, locator, locator_initialization=False, click_on_presence_of_element=False,
                         time_out=HALF_MINUTE):
        if locator_initialization:
            locator = (By.XPATH, locator)
        if click_on_presence_of_element:
            self.wait_for_presence_of_element(locator).click()
        else:
            WebDriverWait(self.driver, time_out).until(EC.presence_of_element_located(locator),
                                                       "Web element was not available within the specific time out. "
                                                       "Locator: '" + str(locator) + "'")
            self.wait_for_element_to_be_clickable(locator).click()

    def click_on_three_dot_option(self, option_name, parent_attribute_value=""):
        if parent_attribute_value == "":
            locator = (By.XPATH, "//a[@title='" + option_name + "']")
        else:
            locator = (
            By.XPATH, "//*[contains(@class, '" + parent_attribute_value + "')]//a[@title='" + option_name + "']")
        self.click_on_element(locator)

    def set_value_into_element(self, locator, text, locator_initialization=False):
        if locator_initialization:
            locator = (By.XPATH, locator)
        WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(locator),
                                             "Web element was not available within the specific time out. "
                                             "Locator: '" + str(locator) + "'")
        self.clear_field(locator)
        self.wait_for_presence_of_element(locator).send_keys(text)

    def clear_field(self, locator):
        self.wait_for_presence_of_element(locator).clear()

    def select_dropdown_value(self, dropdown_label, dropdown_item="", select_by_value=False, value="1", index=1):
        locator = "(//label[contains(text(), '" + dropdown_label + "')]/..//select)[" + str(index) + "]"
        self.dropdown_selection(locator, dropdown_item, select_by_value, value)

    def select_dropdown_value_from_div(self, attribute_type, attribute_value, dropdown_item="", select_by_value=False,
                                       value="1",
                                       tag_name="div"):
        locator = "//" + tag_name + "[@" + attribute_type + "='" + attribute_value + "']/..//select"
        self.dropdown_selection(locator, dropdown_item, select_by_value, value)

    def dropdown_selection(self, locator, dropdown_item="", select_by_value=False, value="1"):
        self.wait_for_presence_of_element((By.XPATH, locator))
        self.wait_for_element_to_be_clickable((By.XPATH, locator))
        if select_by_value:
            Select(self.driver.find_element(By.XPATH, locator)).select_by_value(value)
        else:
            Select(self.driver.find_element(By.XPATH, locator)).select_by_visible_text(dropdown_item)

    def deselect_all_dropdown_value(self, dropdown_label):
        locator = "//label[contains(text(), '" + dropdown_label + "')]/..//select"
        self.wait_for_presence_of_element((By.XPATH, locator))
        self.wait_for_element_to_be_clickable((By.XPATH, locator))
        Select(self.driver.find_element(By.XPATH, locator)).deselect_all()

    def deselect_dropdown_value(self, dropdown_label, dropdown_item="", select_by_value=False, value="1"):
        locator = "//label[contains(text(), '" + dropdown_label + "')]/..//select"
        self.wait_for_presence_of_element((By.XPATH, locator))
        self.wait_for_element_to_be_clickable((By.XPATH, locator))
        if select_by_value:
            Select(self.driver.find_element(By.XPATH, locator)).deselect_by_value(value)
        else:
            Select(self.driver.find_element(By.XPATH, locator)).deselect_by_visible_text(dropdown_item)

    def get_element_count(self, locator, time_out=HALF_MINUTE):
        element = self.wait_for_presence_of_all_elements_located(locator, time_out)
        return len(element)

    def get_element_text(self, locator, time_out=ONE_MINUTE, locator_initialization=False, input_tag=False):
        if locator_initialization:
            locator = (By.XPATH, locator)
        if input_tag:
            element_text = self.wait_for_visibility_of_element(locator, time_out).get_attribute("value")
        else:
            WebDriverWait(self.driver, time_out).until(EC.presence_of_element_located(locator),
                                                       "Web element was not available within the specific time out. "
                                                       "Locator: '" + str(locator) + "'")
            element_text = self.wait_for_presence_of_element(locator, time_out).text
        return element_text

    def get_checked_element_value_attribute(self, label):
        locator = (By.XPATH, "//label[normalize-space(text())='" + label + "']/..//input[@checked='checked']")
        return self.get_element_text(locator, input_tag=True)

    def is_visible(self, locator, time_out=ONE_MINUTE, locator_initialization=False):
        is_visible = None
        try:
            self.wait_for_visibility_of_element(locator, time_out=time_out,
                                                locator_initialization=locator_initialization)
            is_visible = True
        except:
            is_visible = False
        finally:
            return is_visible

    def is_element_present(self, locator, time_out=HALF_MINUTE, locator_initialization=False):
        is_present = None
        if locator_initialization:
            locator = (By.XPATH, locator)
        try:
            WebDriverWait(self.driver, time_out).until(EC.presence_of_element_located(locator),
                                                       "Web element was not available within the specific time out. "
                                                       "Locator: '" + str(locator) + "'")
            is_present = True
        except:
            is_present = False
        finally:
            return is_present

    def is_element_displayed(self, locator):
        element = self.driver.find_element(By.XPATH, locator)
        return element.is_displayed()

    def get_url(self, url, time_out=HALF_MINUTE):
        self.wait_url_contains(time_out, url)
        return self.driver.current_url

    def go_to_url(self, url):
        self.driver.get(url)

    def go_to_prev_page(self):
        return self.driver.back()

    def hover_on_element(self, locator, time_out=ONE_MINUTE):
        hover = ActionChains(self.driver).move_to_element(self.wait_for_presence_of_element(time_out, locator))
        hover.perform()

    def do_page_up(self, time_out=ONE_MINUTE):
        self.wait_for_presence_of_element((By.TAG_NAME, 'body'), time_out).send_keys(Keys.PAGE_UP)

    def do_page_down(self, time_out=ONE_MINUTE):
        self.wait_for_presence_of_element((By.TAG_NAME, 'body'), time_out).send_keys(Keys.PAGE_DOWN)

    def wait_for_presence_of_element(self, locator, time_out=ONE_MINUTE):
        return WebDriverWait(self.driver, time_out).until(EC.presence_of_element_located(locator),
                                                          "Web element was not present within the specific time "
                                                          "out. "
                                                          "Locator: '" + str(locator) + "'")

    def wait_for_element_to_be_clickable(self, locator, time_out=ONE_MINUTE):
        return WebDriverWait(self.driver, time_out).until(EC.element_to_be_clickable(locator),
                                                          "Web element was not clickable within the specific time "
                                                          "out. Locator: '" + str(locator) + "'")

    def wait_for_visibility_of_element(self, locator, time_out=ONE_MINUTE, locator_initialization=False):
        if locator_initialization:
            locator = (By.XPATH, locator)
        return WebDriverWait(self.driver, time_out).until(EC.visibility_of_element_located(locator),
                                                          "Web element was not visible within the specific time "
                                                          "out. Locator: '" + str(locator) + "'")

    def wait_for_visibility_of_all_elements_located(self, locator, time_out=HALF_MINUTE):
        return WebDriverWait(self.driver, time_out).until(EC.visibility_of_all_elements_located(locator),
                                                          "Web elements were not visible within the specific time "
                                                          "out. Locator: '" + str(locator) + "'")

    def wait_for_presence_of_all_elements_located(self, locator, time_out=HALF_MINUTE):
        return WebDriverWait(self.driver, time_out).until(EC.presence_of_all_elements_located(locator),
                                                          "Web elements were not present within the specific time "
                                                          "out. Locator: '" + str(locator) + "'")

    def wait_url_contains(self, time_out, url):
        return WebDriverWait(self.driver, time_out).until(EC.url_contains(url))

    def wait_alert_is_present(self, time_out=HALF_MINUTE):
        return WebDriverWait(self.driver, time_out).until(EC.alert_is_present(),
                                                          "Alert was not present within the specific time out")

    def accept_alert(self):
        Alert(self.driver).accept()

    def get_alert_text(self):
        alert = Alert(self.driver)
        return alert.text

    def get_current_timestamp(self):
        return datetime.now()

    def is_alert_popup_available(self, time_out=HALF_MINUTE):
        try:
            time.sleep(1)
            WebDriverWait(self.driver, time_out).until(EC.alert_is_present())
            return True
        except:
            return False

    @staticmethod
    def get_current_date_with_specific_format(date_format):
        # Example of some date format:
        #
        # dd/mm/YY = "%d/%m/%Y" = 16/09/2019
        # Textual_month day,  year = "%B %d, %Y" = September 16, 2019
        # mm/dd/y = "%m/%d/%y" = 09/16/19
        # Day month_abbreviation, year = "%d %b, %Y" = 16 Sep, 2019

        today = date.today()
        date1 = today.strftime(date_format)
        return str(date1)

    @staticmethod
    def get_specific_date_with_specific_format(date_format, days_to_add=0, days_to_subtract=0):
        # Example of some date format:
        #
        # dd/mm/YY = "%d/%m/%Y" = 16/09/2019
        # Textual_month day,  year = "%B %d, %Y" = September 16, 2019
        # mm/dd/y = "%m/%d/%y" = 09/16/19
        # Day month_abbreviation, year = "%d %b, %Y" = 16 Sep, 2019

        expected_date = None
        if days_to_add != 0:
            expected_date = dt.datetime.today() + dt.timedelta(days=days_to_add)
        elif days_to_subtract != 0:
            expected_date = dt.datetime.today() - dt.timedelta(days=days_to_subtract)
        date1 = expected_date.strftime(date_format)
        return str(date1)

    def select_specific_date_range(self, field_name, date_range_to_select):
        field_locator = (By.XPATH, "(//label[contains(text(), '" + field_name + "')]/..//input)[1]")
        date_range_locator = (By.XPATH, "//a[contains(text(), '" + date_range_to_select + "')]")
        self.click_on_element(field_locator)
        self.click_on_element(date_range_locator)

    def set_value_into_specific_input_field(self, field_name, text, is_textarea=False, tab_out=False):
        if is_textarea:
            field_locator = (By.XPATH, "//label[normalize-space(text())='" + field_name + "']/..//textarea")
        else:
            field_locator = (By.XPATH, "//label[normalize-space(text())='" + field_name + "']/..//input")
        self.set_value_into_element(field_locator, text)
        if tab_out:
            self.wait_for_presence_of_element(field_locator).send_keys(Keys.TAB)

    def select_from_modal(self, search_text, field_label="", is_delay='no', click_uncheck_all=True):
        field_locator = (
            By.XPATH, "//label[contains(text(), '" + field_label + "')]/..//span[@class='mselect-selection']")
        uncheck_all_button_locator = (
            By.XPATH, "//*[@class='additional-btns']//button[contains(@class, 'uncheck-all')]")
        search_field_locator = (
            By.XPATH, "//*[contains(@class, 'modal-select')]//input[contains(@class, 'search-select')]")
        checkbox_locator = (By.XPATH, "//label[contains(text(), '" + search_text + "')]/../input")
        select_button_locator = (By.XPATH, "//button[@data-bb-handler='confirm']")
        if field_label != "":
            self.wait_for_element_to_be_clickable(field_locator)
            self.click_on_element(field_locator)
        self.wait_for_element_to_be_clickable(uncheck_all_button_locator, self.HALF_MINUTE)
        time.sleep(self.TWO_SEC_DELAY)
        if click_uncheck_all:
            self.click_on_element(uncheck_all_button_locator)
        self.wait_for_presence_of_element(search_field_locator)
        self.set_value_into_element(search_field_locator, search_text)
        self.wait_for_element_to_be_clickable(checkbox_locator, self.HALF_MINUTE)
        time.sleep(self.TWO_SEC_DELAY)
        self.click_on_element(checkbox_locator)
        if is_delay == 'yes':
            time.sleep(self.TWO_SEC_DELAY)
        self.click_on_element(select_button_locator)

    def select_from_modal_for_multiple_country(self, search_text, field_label="", is_delay='no'):
        field_locator = (
            By.XPATH, "//label[contains(text(), '" + field_label + "')]/..//span[@class='mselect-selection']")
        search_field_locator = (
            By.XPATH, "//*[contains(@class, 'modal-select')]//input[contains(@class, 'search-select')]")
        checkbox_locator = (By.XPATH, "//label[normalize-space(text())='" + search_text + "']/../input")
        select_button_locator = (By.XPATH, "//button[@data-bb-handler='confirm']")

        if field_label != "":
            self.wait_for_element_to_be_clickable(field_locator)
            self.click_on_element(field_locator)
        self.set_value_into_element(search_field_locator, search_text)
        time.sleep(self.TWO_SEC_DELAY)
        self.wait_for_element_to_be_clickable(checkbox_locator, self.HALF_MINUTE)
        self.click_on_element(checkbox_locator)
        if is_delay == 'yes':
            time.sleep(self.TWO_SEC_DELAY)
        self.click_on_element(select_button_locator)

    def select_multiple_item_from_modal(self, search_text_list, field_label=""):
        field_locator = (
            By.XPATH, "//label[contains(text(), '" + field_label + "')]/..//span[@class='mselect-selection']")
        uncheck_all_button_locator = (
            By.XPATH, "//*[@class='additional-btns']//button[contains(@class, 'uncheck-all')]")
        search_field_locator = (
            By.XPATH, "//*[contains(@class, 'modal-select')]//input[contains(@class, 'search-select')]")
        select_button_locator = (By.XPATH, "//button[@data-bb-handler='confirm']")

        if field_label != "":
            self.wait_for_element_to_be_clickable(field_locator)
            self.click_on_element(field_locator)
        self.wait_for_element_to_be_clickable(uncheck_all_button_locator, self.HALF_MINUTE)
        self.click_on_element(uncheck_all_button_locator)
        for search_text in search_text_list:
            checkbox_locator = (By.XPATH, "//label[normalize-space(text())='" + search_text + "']/../input")
            self.set_value_into_element(search_field_locator, search_text)
            time.sleep(self.TWO_SEC_DELAY)
            self.wait_for_element_to_be_clickable(checkbox_locator, self.HALF_MINUTE)
            self.click_on_element(checkbox_locator)
        self.click_on_element(select_button_locator)

    def get_selected_multiple_items_from_modal(self, field_label):
        selected_checkboxes = []
        field_locator = (
            By.XPATH, "//label[contains(text(), '" + field_label + "')]/..//span[@class='mselect-selection']")
        show_all_button_locator = (
            By.XPATH, "//*[@class='additional-btns']//button[contains(@class, 'get-selected')]")
        cancel_button_locator = (
            By.XPATH, "//button[text()='CANCEL']")
        checked_checkbox_locators = (
            By.XPATH, "//div[@class='bootbox-body']//ul[@class='select-items']//li[@class='select-item']//input")
        self.wait_for_element_to_be_clickable(field_locator)
        self.click_on_element(field_locator)
        self.click_on_element(show_all_button_locator)
        checked_checkbox_elements = self.wait_for_presence_of_all_elements_located(checked_checkbox_locators)
        for checked_checkbox_element in checked_checkbox_elements:
            if checked_checkbox_element.is_selected():
                index = checked_checkbox_elements.index(checked_checkbox_element) + 1
                checked_checkbox_locator = (
                    By.XPATH,
                    "(//div[@class='bootbox-body']//ul[@class='select-items']//li[@class='select-item']//input/following-sibling::label)[" + str(
                        index) + "]")
                checked_checkbox_element = self.wait_for_presence_of_element(checked_checkbox_locator)
                selected_checkboxes.append(checked_checkbox_element.text)
        self.click_on_element(cancel_button_locator)
        return selected_checkboxes

    def check_uncheck_specific_checkbox(self, checkbox_name, do_check, value="", index="1", without_text=False):
        if without_text:
            if value != "":
                checkbox_locator = "//label[normalize-space()='" + checkbox_name + "']/..//input[@value='" + value + "'] | //label[text()='" + checkbox_name + "']/..//input[@value='" + value + "']"
            else:
                checkbox_locator = "(//*[normalize-space()='" + checkbox_name + "']/..//input | //*[text(" \
                                                                                ")='" + checkbox_name + \
                                   "']/..//input)[" + str(index) + "]"
        else:
            if value != "":
                checkbox_locator = "//label[normalize-space(text())='" + checkbox_name + "']/..//input[@value='" + value + "'] | //label[text()='" + checkbox_name + "']/..//input[@value='" + value + "']"
            else:
                checkbox_locator = "(//*[normalize-space(text())='" + checkbox_name + "']/..//input | //*[text(" \
                                                                                      ")='" + checkbox_name + \
                                   "']/..//input)[" + str(index) + "]"
        checkbox_locator = (By.XPATH, checkbox_locator)
        element = self.wait_for_presence_of_element(checkbox_locator)
        if element.is_selected() != do_check:
            self.click_on_element(checkbox_locator)

    def get_text_using_tag_attribute(self, tag_name, attribute_name, attribute_value, time_out=HALF_MINUTE):
        locator = (By.XPATH, "//" + tag_name + "[@" + attribute_name + "='" + attribute_value + "']")
        if tag_name == "input":
            text = self.wait_for_presence_of_element(locator).get_attribute('value')
        else:
            WebDriverWait(self.driver, time_out).until(EC.presence_of_element_located(locator),
                                                       "Web element was not available within the specific time out. "
                                                       "Locator: '" + str(locator) + "'")
            text = self.wait_for_presence_of_element(locator).text
        return text

    def set_text_using_tag_attribute(self, tag_name, attribute_name, attribute_value, input_value,
                                     index=1):
        locator_string = "(//" + tag_name + "[@" + attribute_name + "='" + attribute_value + "'])[" + str(index) + "]"
        locator = (By.XPATH, locator_string)
        self.set_value_into_element(locator, input_value)

    def get_text_or_value_from_selected_option(self, dropdown_label, value=False):

        locators = (By.XPATH, "//label[contains(text(), '" + dropdown_label + "')]/..//select//option")
        elements = self.wait_for_presence_of_all_elements_located(locators)
        option = ""
        for index in range(len(elements)):
            if elements[index].is_selected():
                if value:
                    option = str(elements[index].get_attribute('value')).strip()
                else:
                    option = str(elements[index].text).strip()
        return option

    def get_selected_value_of_modal_from_field(self, select_tag_id_or_class="", field_label="", select_any_value=False):
        if field_label == "":
            locator = (By.XPATH,
                       "//select[@id='" + select_tag_id_or_class + "']/following-sibling::span//span[@class='mselect-selection__rendered selected'] | "
                                                                   "//select[@class='" + select_tag_id_or_class + "']/following-sibling::span//span[@class='mselect-selection__rendered selected']")
        else:
            if select_any_value:
                locator = (By.XPATH, "//label[contains(text(), '" + field_label + "')]/..//span["
                                                                                  "@class='mselect-selection__rendered']")
            else:
                locator = (By.XPATH, "//label[contains(text(), '" + field_label + "')]/..//span["
                                                                                  "@class='mselect-selection__rendered selected']")

        return self.wait_for_presence_of_element(locator).text

    def get_selected_checkbox_name_from_a_section(self, section_div_id, label_is_parent=False, span_is_present=False,
                                                  multiple=False):
        locators = (By.XPATH, "//div[@id='" + section_div_id + "']//input[@type='checkbox']")
        elements = self.wait_for_presence_of_all_elements_located(locators)
        if multiple:
            checkbox_names = []
            for index in range(len(elements)):
                if elements[index].is_selected():
                    locator = "(//div[@id='" + section_div_id + "']//input[@type='checkbox'])[" + str(
                        index + 1) + "]/.."
                    if label_is_parent:
                        checkbox_names.append(str(self.wait_for_presence_of_element((By.XPATH, locator)).text).strip())
                    elif span_is_present:
                        checkbox_names.append(
                            str(self.wait_for_presence_of_element((By.XPATH, locator + "//span")).text).strip())
                    else:
                        checkbox_names.append(
                            str(self.wait_for_presence_of_element((By.XPATH, locator + "//label")).text).strip())
            return checkbox_names
        else:
            checkbox_name = ""
            for index in range(len(elements)):
                if elements[index].is_selected():
                    locator = "(//div[@id='" + section_div_id + "']//input[@type='checkbox'])[" + str(
                        index + 1) + "]/.."
                    if label_is_parent:
                        checkbox_name = str(self.wait_for_presence_of_element((By.XPATH, locator)).text).strip()
                    elif span_is_present:
                        checkbox_name = str(
                            self.wait_for_presence_of_element((By.XPATH, locator + "//span")).text).strip()
                    else:
                        checkbox_name = str(
                            self.wait_for_presence_of_element((By.XPATH, locator + "//label")).text).strip()
            return checkbox_name

    def get_checkbox_status(self, checkbox_name, value="", without_text=False):
        if without_text:
            if value != "":
                checkbox_locator = "//label[normalize-space()='" + checkbox_name + "']/..//input[@value='" + value + "'] | //label[text()='" + checkbox_name + "']/..//input[@value='" + value + "']"
            else:
                checkbox_locator = "//label[normalize-space()='" + checkbox_name + "']/..//input | //label[text()='" + checkbox_name + "']/..//input"
        else:
            if value != "":
                checkbox_locator = "//label[normalize-space(text())='" + checkbox_name + "']/..//input[@value='" + value + "'] | //label[text()='" + checkbox_name + "']/..//input[@value='" + value + "']"
            else:
                checkbox_locator = "//label[normalize-space(text())='" + checkbox_name + "']/..//input | //label[text()='" + checkbox_name + "']/..//input"
        checkbox_locator = (By.XPATH, checkbox_locator)
        element = self.wait_for_presence_of_element(checkbox_locator)
        if element.is_selected():
            return 'True'
        else:
            return ''

    def check_uncheck_specific_grid_row_checkbox(self, parent_div_id, check_the_checkbox,
                                                 check_all_checkbox=False, column_value_to_identify_column=""):
        if check_all_checkbox:
            checkbox_locator = "(//div[@id='" + parent_div_id + "']//tr[1]//input[@type='checkbox'])[1]"
        else:
            checkbox_locator = "//div[@id='" + parent_div_id + "']//a[normalize-space()='" + column_value_to_identify_column + "']/..//..//..//input[@type='checkbox']"
        checkbox_locator = (By.XPATH, checkbox_locator)
        element = self.wait_for_presence_of_element(checkbox_locator)
        if element.is_selected() != check_the_checkbox:
            self.click_on_element(checkbox_locator)

    def select_item_from_multi_action_menu(self, action_button_id, item_name_to_select):
        actions_locator = (By.XPATH, "//*[@id='" + action_button_id + "']")
        self.click_on_element(actions_locator)
        actions_item_locator = (By.XPATH, "//a[@title='" + item_name_to_select + "']")
        self.click_on_element(actions_item_locator)

    def switch_to_new_window(self):
        time.sleep(self.TWO_SEC_DELAY)
        self.driver.switch_to.window(self.driver.window_handles[1])

    def close_the_current_window_and_back_to_previous_window(self):
        self.driver.close()
        time.sleep(self.TWO_SEC_DELAY)
        self.driver.switch_to.window(self.driver.window_handles[0])

    def get_specific_form_grid_column_index(self, form_tag_id, column_name):
        index = 0
        locators = (By.XPATH, "//form[@id='" + form_tag_id + "']//tr[1]//th")
        elements = self.wait_for_presence_of_all_elements_located(locators)
        for index in range(len(elements)):
            column_locator = (By.XPATH, "//form[@id='" + form_tag_id + "']//tr[1]//th[" + str(index + 1) + "]")
            if self.get_element_text(column_locator) == column_name:
                index = index + 1
                break
        return index

    def set_value_into_specific_form_grid_input_field(self, form_tag_id, column_name, column_value_to_set,
                                                      row_number="1"):
        index = self.get_specific_form_grid_column_index(form_tag_id, column_name)
        locator = (By.XPATH, "//form[@id='" + form_tag_id + "']//tbody//tr[" + row_number + "]//td[" + str(
            index) + "]//input")
        self.set_value_into_element(locator, column_value_to_set)

    def select_dropdown_value_from_specific_form_grid(self, form_tag_id, column_name,
                                                      column_value_to_select, row_number="1",
                                                      search_option_available=True):
        index = self.get_specific_form_grid_column_index(form_tag_id, column_name)
        dropdown_icon_locator = (By.XPATH,
                                 "//form[@id='" + form_tag_id + "']//tbody//tr[" + row_number + "]//td[" + str(
                                     index) + "]//span[@role='presentation']")
        self.click_on_element(dropdown_icon_locator)
        if search_option_available:
            input_field_locator = (
                By.XPATH,
                "//span[@class='select2-search select2-search--dropdown']//input[@class='select2-search__field']")
            self.set_value_into_element(input_field_locator, column_value_to_select)
            self.wait_for_presence_of_element(input_field_locator).send_keys(Keys.ENTER)
        else:
            self.wait_for_presence_of_element(
                (By.XPATH, "//li[normalize-space()='" + column_value_to_select + "']")).click()

    def select_value_from_specific_form_grid_modal(self, form_tag_id, column_name,
                                                   column_value_to_select, row_number="1"):
        index = self.get_specific_form_grid_column_index(form_tag_id, column_name)
        dropdown_icon_locator = (By.XPATH,
                                 "//form[@id='" + form_tag_id + "']//tbody//tr[" + row_number + "]//td[" + str(
                                     index) + "]//span[@role='presentation']")
        self.click_on_element(dropdown_icon_locator)
        self.select_from_modal(column_value_to_select)

    def check_uncheck_specific_form_grid_row_checkbox(self, form_tag_id, column_name,
                                                      check_the_checkbox, row_number="1"):
        index = self.get_specific_form_grid_column_index(form_tag_id, column_name)
        checkbox_locator = (By.XPATH,
                            "//form[@id='" + form_tag_id + "']//tbody//tr[" + row_number + "]//td[" + str(
                                index) + "]//input[@type='checkbox']")
        element = self.wait_for_presence_of_element(checkbox_locator)
        if element.is_selected() != check_the_checkbox:
            self.click_on_element(checkbox_locator)

    def deselect_all_options_from_grid_modal(self, locator):
        self.wait_for_presence_of_element((By.XPATH, locator))
        self.wait_for_element_to_be_clickable((By.XPATH, locator))
        Select(self.driver.find_element(By.XPATH, locator)).deselect_all()

    def check_uncheck_specific_form_grid_row_checkbox_modal(self, checkbox_name, do_check, value="", row_number="1"):
        if value != "":
            checkbox_locator = "(// label[normalize-space(text())='" + checkbox_name + "'] /..// input[ @value = '" + value + "'])[" + row_number + "] | (// label[text() = '" + checkbox_name + "'] /..// input[ @value = '" + value + "'])[" + row_number + "]"
        else:
            checkbox_locator = "(//input[@data-name='" + checkbox_name + "'])[" + row_number + "]"
        checkbox_locator = (By.XPATH, checkbox_locator)
        element = self.wait_for_presence_of_element(checkbox_locator)
        if element.is_selected() != do_check:
            self.click_on_element(checkbox_locator)

    def click_link_of_specific_column_of_specific_row_from_grid(self, form_tag_id, column_name, row_number="1"):
        index = self.get_specific_form_grid_column_index(form_tag_id, column_name)
        locator = (By.XPATH, "//form[@id='" + form_tag_id + "']//tbody//tr[" + row_number + "]//td[" + str(
            index) + "]//div")
        self.click_on_element(locator)

    def click_ok_button_of_specific_column_modal_from_grid(self, form_tag_id, column_name, row_number="1"):
        index = self.get_specific_form_grid_column_index(form_tag_id, column_name)
        locator = (By.XPATH, "//form[@id='" + form_tag_id + "']//tbody//tr[" + row_number + "]//td[" + str(
            index) + "]//button[@class='btn btn-primary js-modal-data-save']")
        self.click_on_element(locator)

    def wait_for_element_to_be_invisible(self, locator, time_out=ONE_MINUTE):
        return WebDriverWait(self.driver, time_out).until(EC.invisibility_of_element_located(locator))

    def click_element_execute_script(self, locator, locator_initialize=False):
        if locator_initialize:
            (method, locator) = locator
            element = self.driver.find_element(By.XPATH, locator)
            self.driver.execute_script("arguments[0].click();", element)
        else:
            element = self.driver.find_element(By.XPATH, locator)
            self.driver.execute_script("arguments[0].click();", element)

    def click_on_specific_tab(self, tab_name):
        tab_locator = (By.XPATH, "//a[normalize-space()='" + tab_name + "' and @data-toggle='tab']")
        self.click_on_element(tab_locator)

    def switch_to_iframe(self, locator, is_element=False):
        self.driver.switch_to_default_content()
        if is_element:
            iframe = locator
        else:
            iframe = self.wait_for_presence_of_element(locator)
        self.driver.switch_to.frame(iframe)
        time.sleep(self.TWO_SEC_DELAY)

    def get_attribute_value(self, locator, attribute_name, locator_initialization=False):
        if locator_initialization:
            locator = (By.XPATH, locator)
        return self.wait_for_presence_of_element(locator).get_attribute(attribute_name)

    def click_on_specific_button(self, name_name, script_executor_click=False):
        button_locator = "//button[normalize-space(text())='" + name_name + "'] | //a[normalize-space(text())='" + name_name + "']"
        if script_executor_click:
            self.click_element_execute_script(button_locator)
        else:
            self.click_on_element(button_locator, locator_initialization=True)

    def get_specific_grid_column_index(self, div_id, column_name):
        index = 0
        locators = (By.XPATH, "//div[@id='" + div_id + "']//tr[1]//th")
        elements = self.wait_for_presence_of_all_elements_located(locators)
        for index in range(len(elements)):
            column_locator = (By.XPATH, "//div[@id='" + div_id + "']//tr[1]//th[" + str(index + 1) + "]")
            if self.get_element_text(column_locator) == column_name:
                index = index + 1
                break
        return index

    def get_value_from_specific_grid_column(self, div_id, column_name, a_tag=False, row_number="1"):
        index = self.get_specific_grid_column_index(div_id, column_name)
        if a_tag:
            locator = (
                By.XPATH, "//div[@id='" + div_id + "']//tbody//tr[" + row_number + "]//td[" + str(index) + "]//a")
        else:
            locator = (By.XPATH, "//div[@id='" + div_id + "']//tbody//tr[" + row_number + "]//td[" + str(
                index) + "]")
        value = self.get_element_text(locator)
        return str(value)

    def is_image_present(self, locator):
        element = self.driver.find_element(By.XPATH, locator)
        status = self.driver.execute_script(
            "return arguments[0].complete " + "&& typeof arguments[0].naturalWidth != \"undefined\" " + "&& arguments[0].naturalWidth > 0",
            element)
        return status

    def get_value_from_specific_input_field(self, field_name, is_textarea=False, inner_html=False):
        if is_textarea:
            field_locator = (By.XPATH, "//label[normalize-space(text())='" + field_name + "']/..//textarea")
        else:
            field_locator = (By.XPATH, "//label[normalize-space(text())='" + field_name + "']/..//input")
        if is_textarea is False:
            text = self.wait_for_presence_of_element(field_locator).get_attribute('value')
        elif inner_html:
            text = self.wait_for_presence_of_element(field_locator).get_attribute("innerHTML")
        else:
            text = self.wait_for_presence_of_element(field_locator).text
        return text

    def select_specific_radio_button(self, radio_button_name):
        locator = (By.XPATH, "//label[normalize-space()='" + radio_button_name + "']//input")
        self.click_on_element(locator)

    def is_specific_field_enabled(self, field_name, is_input_field=False):
        if is_input_field:
            locator = "//label[normalize-space()='" + field_name + "']/..//input"
            element = self.driver.find_element(By.XPATH, locator)
            status = element.get_attribute('readonly')
            return not status
        else:
            locator = "//label[normalize-space()='" + field_name + "']/..//select"
            element = self.driver.find_element(By.XPATH, locator)
            return element.is_enabled()
