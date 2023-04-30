from pages.user.user_form import DashboardUserFormPage
from pages.user.bulk_user_add_form import DashboardBulkUserAddFormPage
from pages.user.bulk_user_signup_form import DashboardBulkUserSignUpFormPage
from pages.user.user_list_form import DashboardUserListForm
from pages.sidebar.sidebar import DashboardSidebarPage
from pages.navbar.navbar import DashboardNavbar
from pages.index.index import DspDashboardIndex
from configurations import generic_modules, mysql
import json
from utils.user import UserUtils as UserUtil
from utils.compare import CompareUtils as CompareUtil
import pytest
import os

@pytest.mark.skipif("JENKINS_URL" in os.environ, reason="Test need to be run manually")
def test_add_user(login_by_user_type):
    config, driver = login_by_user_type
    user_list_page = DashboardUserListForm(driver)
    user_page = DashboardUserFormPage(driver)
    side_bar_navigation = DashboardSidebarPage(driver)
    navbar = DashboardNavbar(driver)
    index_page = DspDashboardIndex(config, driver)
    with open('assets/user/user_data.json') as json_file:
        user_data = json.load(json_file)
    user_data['main_and_billing_info']['username'] = user_data['main_and_billing_info'][
                                                         'username'] + generic_modules.get_random_string()
    generated_password = generic_modules.get_random_string(10)
    # ADD USER
    side_bar_navigation.navigate_to_admin_user_page()
    user_list_page.navigate_to_add_user_page()
    user_page.provide_and_save_user_information(user_data, generated_password)
    user_list_page.search_user_and_action(user_data['main_and_billing_info']['username'], action='edit')
    pulled_gui_data = user_page.get_user_information()
    user_list_page.wait_for_loader_to_be_invisible()
    assert "All data verification is successful" == CompareUtil.verify_data(pulled_gui_data, user_data)
    # LOGIN CHECK
    navbar.logout_user()
    index_page.login_user(user_data['main_and_billing_info']['username'], generated_password)
    assert "Eskimi DSP - Your programmatic partner" in index_page.get_page_title()
    navbar.logout_user()
    index_page.login()
    side_bar_navigation.navigate_to_admin_user_page()
    # CLEAN UP
    user_list_page.search_user_and_action(user_data['main_and_billing_info']['username'], action='delete')
    assert "User deleted!" in user_list_page.get_success_message()


@pytest.mark.skipif(mysql.mysql_connection_test(), reason="Couldn't establish MySQL connection")
def test_bulk_user(login_by_user_type):
    config, driver = login_by_user_type
    bulk_user_add_page = DashboardBulkUserAddFormPage(driver)
    bulk_user_signup_page = DashboardBulkUserSignUpFormPage(driver)
    user_list_page = DashboardUserListForm(driver)
    user_page = DashboardUserFormPage(driver)
    side_bar_navigation = DashboardSidebarPage(driver)
    index_page = DspDashboardIndex(config, driver)
    navbar = DashboardNavbar(driver)
    with open('assets/user/bulk_user_data.json') as json_file:
        bulk_user_data = json.load(json_file)
    bulk_user_data['email'] = bulk_user_data['email'].format(generic_modules.get_random_string(6))
    generated_password = generic_modules.get_random_string(10)
    # ADD BULK USER
    side_bar_navigation.navigate_to_admin_user_page()
    user_list_page.navigate_to_bulk_user_page()
    bulk_user_add_page.provide_bulk_user_information(bulk_user_data)
    assert "Successful send email invitations" in user_list_page.get_success_message()
    debug_mode = "JENKINS_URL" not in os.environ
    if debug_mode:
        # THIS CODE SHOULD NOT RUN IN HEADLESS MODE BECAUSE OF RECAPTCHA
        # RETRIEVE INVITATION URL
        driver.get(UserUtil.get_bulk_user_url(bulk_user_data['email']))
        bulk_user_signup_page.provide_bulk_user_signup_information(bulk_user_data, generated_password)
        bulk_user_signup_page.click_login_button_after_signup()
        # DATA VERIFICATION
        with open('assets/user/bulk_user_verification_data.json') as json_file:
            bulk_user_verification_data = json.load(json_file)
        bulk_user_verification_data['main_and_billing_info']['username'] = bulk_user_data['email']
        bulk_user_verification_data['main_and_billing_info']['email'] = bulk_user_data['email']
        bulk_user_verification_data['main_and_billing_info']['contact_person_email'] = bulk_user_data['email']
        side_bar_navigation.navigate_to_admin_user_page()
        user_list_page.search_user_and_action(bulk_user_data['email'], "Edit")
        pulled_gui_data = user_page.get_user_information()
        user_list_page.wait_for_loader_to_be_invisible()
        assert "All data verification is successful" == CompareUtil.verify_data(pulled_gui_data, bulk_user_verification_data)
        # LOGIN CHECK
        navbar.logout_user()
        index_page.login_user(bulk_user_data['email'], generated_password)
        assert "Eskimi DSP - Your programmatic partner" in index_page.get_page_title()
        navbar.logout_user()
        index_page.login()
        side_bar_navigation.navigate_to_admin_user_page()
        # CLEAN UP
        user_list_page.search_user_and_action(bulk_user_data['email'], action='delete')
        assert "User deleted!" in user_list_page.get_success_message()
    else:
        assert True
