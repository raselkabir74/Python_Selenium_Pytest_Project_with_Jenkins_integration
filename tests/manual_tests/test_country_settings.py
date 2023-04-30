import json
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.country_settings.country_settings_list import DashboardCountrySettingsList
from utils.compare import CompareUtils as CompareUtil


def test_country_settings(login_by_user_type):
    config, driver = login_by_user_type
    sidebar_navigation = DashboardSidebarPage(driver)
    country_settings_page = DashboardCountrySettingsList(driver)
    with open('assets/country_settings/country_settings_data.json') as json_file:
        country_settings_data = json.load(json_file)
    sidebar_navigation.navigate_to_country_settings()
    country_settings_page.add_country_settings(country_settings_data)
    assert "Saved successfully." in country_settings_page.get_success_message()
    pulled_country_settings_data = country_settings_page.get_country_settings_data(country_settings_data)
    assert "All data verification is successful" == CompareUtil.verify_data(pulled_country_settings_data, country_settings_data)
    country_settings_page.delete_country_settings(country_settings_data)
    assert "Saved successfully." in country_settings_page.get_success_message()

