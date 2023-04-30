import json
from configurations.generic_modules import get_random_string
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.billing_entities.billing_entities_form import DashboardBillingEntitiesForm
from pages.billing_entities.billing_entities_list import DashboardBillingEntitiesList
from utils.compare import CompareUtils as CompareUtil


def test_billing_entities(login_by_user_type):
    config, driver = login_by_user_type
    sidebar_navigation = DashboardSidebarPage(driver)
    billing_entities_list_page = DashboardBillingEntitiesList(driver)
    billing_entities_form_page = DashboardBillingEntitiesForm(driver)
    with open('assets/billing_entities/billing_entities.json') as json_file:
        billing_entities_data = json.load(json_file)
    billing_entities_data['title'] = billing_entities_data['title'] + get_random_string()
    sidebar_navigation.navigate_to_eskimi_billing_entities()
    billing_entities_list_page.navigate_to_billing_entities_form()
    billing_entities_form_page.provide_and_save_data(billing_entities_data)
    assert "Profile saved successfully!" in billing_entities_list_page.get_success_message()
    billing_entities_list_page.action_billing_entities(billing_entities_data['title'], is_edit=True)
    pulled_gui_data = billing_entities_form_page.get_billing_entities_data()
    assert "All data verification is successful" == CompareUtil.verify_data(pulled_gui_data, billing_entities_data)
    billing_entities_list_page.action_billing_entities(billing_entities_data['title'])
    assert "No matching records found" in billing_entities_list_page.get_empty_search_result_text(
        billing_entities_data['title'])
