import json
from configurations.generic_modules import get_random_string
from pages.package.packages_form import DashboardPackagesForm
from pages.package.packages_list import DashboardPackagesList
from pages.sidebar.sidebar import DashboardSidebarPage
from utils.packages import PackagesUtils as PackageUtil
from utils.compare import CompareUtils as CompareUtil


def test_add_and_edit_package(login_by_user_type):
    config, driver = login_by_user_type
    package_list_page = DashboardPackagesList(driver)
    package_form_page = DashboardPackagesForm(driver)
    side_bar_page = DashboardSidebarPage(driver)
    with open('assets/packages/package_data.json') as json_file:
        package_data = json.load(json_file)
    package_data['name'] = package_data['name'] + get_random_string()
    package_data['sites'] = PackageUtil.read_site_domain_names()
    with open('assets/packages/edit_package_data.json') as json_file:
        edit_package_data = json.load(json_file)
    edit_package_data['name'] = edit_package_data['name'] + get_random_string()
    edit_package_data['sites'] = PackageUtil.read_site_domain_names(operation='edit')
    # ADD PACKAGE
    side_bar_page.navigate_to_packages()
    package_list_page.navigate_add_package()
    package_form_page.provide_package_data_and_save(package_data)
    success_message = package_list_page.get_success_message()
    assert "Package saved successfully! Package size will be calculated shortly." in success_message
    # VERIFY ADD PACKAGE DATA
    package_list_page.edit_package(package_data['name'])
    pulled_gui_data = package_form_page.get_package_data()
    assert "All data verification is successful" == CompareUtil.verify_data(pulled_gui_data, package_data)
    # EDIT PACKAGE DATA
    package_list_page.edit_package(package_data['name'])
    package_form_page.provide_package_data_and_save(edit_package_data)
    success_message = package_list_page.get_success_message()
    assert "Package saved successfully!" in success_message
    # VERIFY EDIT PACKAGE DATA
    package_list_page.edit_package(edit_package_data['name'])
    pulled_gui_data = package_form_page.get_package_data(operation='edit')
    assert "All data verification is successful" == CompareUtil.verify_data(pulled_gui_data, edit_package_data)
    # PACKAGE CLEAN UP
    package_list_page.delete_package(edit_package_data['name'])
    success_message = package_list_page.get_success_message()
    assert "Successfully deleted 1 Packages" in success_message

