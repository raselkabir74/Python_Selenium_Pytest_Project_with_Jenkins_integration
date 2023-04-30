from selenium.webdriver.common.by import By

from locators.package.package_form_locator import PackageFormLocators
from pages.base_page import BasePage
from selenium.webdriver.support.select import Select
import os

package_information = {}


class DashboardPackagesForm(BasePage):
    def __init__(self, driver):
        super().__init__(driver)

    def provide_package_data_and_save(self, package_data):
        self.set_value_into_specific_input_field(PackageFormLocators.package_name_label, package_data['name'])
        self.select_dropdown_value(PackageFormLocators.auction_type_label, package_data['auction_type'])
        self.set_value_into_specific_input_field(PackageFormLocators.csv_upload_label,
                                                 os.path.join(os.getcwd(), package_data['csv_upload']))
        self.select_from_modal(package_data['user'], PackageFormLocators.user_label, is_delay='yes')
        self.click_on_element(PackageFormLocators.save_button_locator)

    def get_package_data(self, operation='add'):
        package_information['name'] = self.get_text_using_tag_attribute(self.input_tag, self.name_attribute,
                                                                        PackageFormLocators.package_field_name)
        package_information['auction_type'] = self.get_text_or_value_from_selected_option(
            PackageFormLocators.auction_type_label)
        if operation == 'edit':
            package_information['csv_upload'] = 'assets/packages/edit_package_sites.csv'
        else:
            package_information['csv_upload'] = 'assets/packages/package_sites.csv'
        package_information['user'] = self.get_text_using_tag_attribute(self.span_tag, self.class_attribute,
                                                                        PackageFormLocators.user_field_class)
        package_information['sites'] = self.get_packages_sites()
        self.click_on_element(PackageFormLocators.cancel_button_locator)
        return package_information

    def get_packages_sites(self):
        sites = []
        for option in Select(self.driver.find_element(By.ID, PackageFormLocators.selected_site_list_id)).options:
            sites.append(option.get_attribute('value'))
        sites.sort()
        return sites
