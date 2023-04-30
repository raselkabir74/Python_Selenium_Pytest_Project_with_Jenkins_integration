import json
from configurations.generic_modules import get_random_string
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.brand_safety.brand_safety_list_form import DashboardBrandSafetyListForm
from pages.brand_safety.brand_safety_form import DashboardBrandSafetyForm
from pages.brand_safety.brand_safety_keywords_list import DashboardBrandSafetyKeywordsList
from utils.compare import CompareUtils as CompareUtil
from utils.brand_safety import BrandSafetyUtils as BrandSafetyUtil


def test_add_edit_brand_safety(login_by_user_type):
    config, driver = login_by_user_type
    sidebar_navigation = DashboardSidebarPage(driver)
    brand_safety_list_page = DashboardBrandSafetyListForm(driver)
    brand_safety_form_page = DashboardBrandSafetyForm(driver)
    brand_safety_keyword_list_page = DashboardBrandSafetyKeywordsList(driver)
    with open('assets/brand_safety/brand_safety_data.json') as json_file:
        brand_safety_data = json.load(json_file)
    brand_safety_data['title'] = brand_safety_data['title'] + get_random_string()
    brand_safety_data = BrandSafetyUtil.process_brand_safety_data(brand_safety_data)
    # ADD BRAND SAFETY
    sidebar_navigation.navigate_to_brand_safety()
    brand_safety_list_page.navigate_to_add_brand_safety_page()
    brand_safety_form_page.provide_and_save_brand_safety_data(brand_safety_data)
    # VERIFY ADD BRAND SAFETY DATA
    brand_safety_list_page.search(brand_safety_data['title'])
    brand_safety_list_page.navigate_to_edit_brand_safety(brand_safety_data['title'])
    pulled_brand_safety_information = brand_safety_form_page.get_brand_safety_information()
    assert "All data verification is successful" == CompareUtil.verify_data(pulled_brand_safety_information,
                                                                            brand_safety_data)
    # EDIT BRAND SAFETY
    with open('assets/brand_safety/brand_safety_edit_data.json') as json_file:
        edit_brand_safety_data = json.load(json_file)
    edit_brand_safety_data['title'] = edit_brand_safety_data['title'] + get_random_string()
    edit_brand_safety_data = BrandSafetyUtil.process_brand_safety_data(edit_brand_safety_data)
    brand_safety_form_page.provide_and_save_brand_safety_data(edit_brand_safety_data)
    pulled_brand_edit_safety_information = brand_safety_form_page.get_brand_safety_information()
    assert "All data verification is successful" == CompareUtil.verify_data(pulled_brand_edit_safety_information,
                                                                            edit_brand_safety_data)
    brand_safety_form_page.cancel_form()
    brand_safety_list_page.search(edit_brand_safety_data['title'])
    brand_safety_list_page.navigate_to_keyword_count_page(edit_brand_safety_data['title'])
    # KEYWORDS VERIFICATION, ADD and EDIT
    pulled_keywords_list = brand_safety_keyword_list_page.getkeywordslist()
    provided_keywords_list = BrandSafetyUtil.get_provided_keyword_list()
    assert "All data verification is successful" == CompareUtil.verify_data(pulled_keywords_list, provided_keywords_list)
    new_keyword = "Keyword_Add" + get_random_string()
    brand_safety_keyword_list_page.add_keyword(new_keyword)
    success_message = brand_safety_keyword_list_page.get_success_message()
    assert "Successfully added keywords" in success_message
    brand_safety_keyword_list_page.delete_keyword(new_keyword)
    success_message = brand_safety_keyword_list_page.get_success_message()
    assert "Successfully deleted keywords" in success_message
    brand_safety_keyword_list_page.navigate_back_to_brand_safety_list()
    # DELETE BRAND SAFETY
    brand_safety_list_page.search(edit_brand_safety_data['title'])
    brand_safety_list_page.delete_brand_safety(edit_brand_safety_data['title'])
    assert "Successfully deleted brand safety set" in brand_safety_list_page.get_success_message()
