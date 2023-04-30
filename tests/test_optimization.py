import os

from locators.optimization.optimization_locators import OptimizationLocators
from pages.base_page import BasePage
from pages.navbar.navbar import DashboardNavbar
from pages.optimization.optimization import DspDashboardOptimization
from pages.sidebar.sidebar import DashboardSidebarPage


def test_optimization(login_by_user_type):
    config, driver = login_by_user_type
    navbar = DashboardNavbar(driver)
    base_page = BasePage(driver)
    side_bar_navigation = DashboardSidebarPage(driver)
    optimization_page = DspDashboardOptimization(config, driver)
    debug_mode = "JENKINS_URL" not in os.environ

    campaign_id_list = {'*777# DSP campaign - 05 Mar - 08 Apr - Broad - Competitors/Wifi (ID: 73949)',
                        '*777# DSP campaign - 05 Mar - 08 Apr - device price TOP sites - Click to USSD (ID: 73948)',
                        '*777# DSP campaign - 05 Mar - 08 Apr - device price TOP sites - Competitors/Wifi (ID: 73945)'}
    navbar.impersonate_user('Webcoupers - GLO')
    side_bar_navigation.navigate_to_optimisation()
    base_page.select_multiple_item_from_modal(campaign_id_list, OptimizationLocators.campaign_label)
    base_page.select_dropdown_value(OptimizationLocators.spent_label, "", True,
                                    OptimizationLocators.spent_based_on_cost_dropdown_item_value)
    optimization_page.select_specific_date_range_for_optimisation("All,")

    # [START] OPTIMISE BY EXCHANGE
    base_page.select_dropdown_value(OptimizationLocators.optimise_by_label, "", True,
                                    OptimizationLocators.optimise_by_exchange_dropdown_item_value)
    base_page.click_on_element(OptimizationLocators.search_button_locator)
    optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_exchange_dropdown_item_value,
                                                 is_play=True, group_action=True)
    base_page.click_on_element(OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status("1",
                                                                   OptimizationLocators.optimise_by_exchange_dropdown_item_value,
                                                                   "pause", group_and_single_action=True)
    optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_exchange_dropdown_item_value,
                                                 is_play=False, group_action=True)
    base_page.click_on_element(OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status("1",
                                                                   OptimizationLocators.optimise_by_exchange_dropdown_item_value,
                                                                   "play", group_and_single_action=True) 
    if debug_mode:
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_exchange_dropdown_item_value,
                                                     is_play=True, single_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_exchange_dropdown_item_value,
                                                                       "pause", group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_exchange_dropdown_item_value,
                                                     is_play=False, single_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_exchange_dropdown_item_value,
                                                                       "play", group_and_single_action=True)

    optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_exchange_dropdown_item_value,
                                                 is_play=True, group_action=True)
    optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_exchange_dropdown_item_value,
                                                 is_play=True, bulk_action=True)
    base_page.click_on_element(OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status("1",
                                                                   OptimizationLocators.optimise_by_exchange_dropdown_item_value,
                                                                   "pause", bulk_action=True)
    optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_exchange_dropdown_item_value,
                                                 is_play=True, group_action=True)
    optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_exchange_dropdown_item_value,
                                                 is_play=False, bulk_action=True)
    base_page.click_on_element(OptimizationLocators.search_button_locator)
    assert optimization_page.get_specific_play_pause_button_status("1",
                                                                   OptimizationLocators.optimise_by_exchange_dropdown_item_value,
                                                                   "play", bulk_action=True)
    # [END] OPTIMISE BY EXCHANGE

    # FOLLOWING PORTION OF SCRIPTS WILL BE EXECUTED ONLY IN LOCAL RUN. BECAUSE IT MAY OCCURS PROBLEM TO RUN IN
    # JENKINS AS THIS IS A HUGE TEST CASE
    if debug_mode:
        # [START] OPTIMISE BY CREATIVE
        base_page.select_dropdown_value(OptimizationLocators.optimise_by_label, "", True,
                                        OptimizationLocators.optimise_by_creative_dropdown_item_value)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_creative_dropdown_item_value,
                                                     is_play=True, group_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_creative_dropdown_item_value,
                                                                       "pause", group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_creative_dropdown_item_value,
                                                     is_play=False, single_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_creative_dropdown_item_value,
                                                                       "play", group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_creative_dropdown_item_value,
                                                     is_play=True, group_action=True)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_creative_dropdown_item_value,
                                                     is_play=True, bulk_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_creative_dropdown_item_value,
                                                                       "pause", bulk_action=True)

        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_creative_dropdown_item_value,
                                                     is_play=False, group_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_creative_dropdown_item_value,
                                                                       "play", group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_creative_dropdown_item_value,
                                                     is_play=True, single_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_creative_dropdown_item_value,
                                                                       "pause", group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_creative_dropdown_item_value,
                                                     is_play=True, group_action=True)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_creative_dropdown_item_value,
                                                     is_play=False, bulk_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_creative_dropdown_item_value,
                                                                       "play", bulk_action=True)
        # [END] OPTIMISE BY CREATIVE

        # [START] OPTIMISE BY OPERATING SYSTEM
        base_page.select_dropdown_value(OptimizationLocators.optimise_by_label, "", True,
                                        OptimizationLocators.optimise_by_os_dropdown_item_value)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_os_dropdown_item_value,
                                                     is_play=True, group_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_os_dropdown_item_value,
                                                                       "pause", group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_os_dropdown_item_value,
                                                     is_play=False, single_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_os_dropdown_item_value,
                                                                       "play", group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_os_dropdown_item_value,
                                                     is_play=True, group_action=True)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_os_dropdown_item_value,
                                                     is_play=True, bulk_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_os_dropdown_item_value,
                                                                       "pause", bulk_action=True)

        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_os_dropdown_item_value,
                                                     is_play=False, group_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_os_dropdown_item_value,
                                                                       "play", group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_os_dropdown_item_value,
                                                     is_play=True, single_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_os_dropdown_item_value,
                                                                       "pause", group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_os_dropdown_item_value,
                                                     is_play=True, group_action=True)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_os_dropdown_item_value,
                                                     is_play=False, bulk_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_os_dropdown_item_value,
                                                                       "play", bulk_action=True)
        # [END] OPTIMISE BY OPERATING SYSTEM

        # [START] OPTIMISE BY BROWSER
        base_page.select_dropdown_value(OptimizationLocators.optimise_by_label, "", True,
                                        OptimizationLocators.optimise_by_browser_dropdown_item_value)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_browser_dropdown_item_value,
                                                     is_play=True, group_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_browser_dropdown_item_value,
                                                                       "pause", group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_browser_dropdown_item_value,
                                                     is_play=False, single_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_browser_dropdown_item_value,
                                                                       "play", group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_browser_dropdown_item_value,
                                                     is_play=True, group_action=True)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_browser_dropdown_item_value,
                                                     is_play=True, bulk_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_browser_dropdown_item_value,
                                                                       "pause", bulk_action=True)

        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_browser_dropdown_item_value,
                                                     is_play=False, group_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_browser_dropdown_item_value,
                                                                       "play", group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_browser_dropdown_item_value,
                                                     is_play=True, single_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_browser_dropdown_item_value,
                                                                       "pause", group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_browser_dropdown_item_value,
                                                     is_play=True, group_action=True)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_browser_dropdown_item_value,
                                                     is_play=False, bulk_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_browser_dropdown_item_value,
                                                                       "play", bulk_action=True)
        # [END] OPTIMISE BY BROWSER

        # [START] OPTIMISE BY OPERATOR
        base_page.select_dropdown_value(OptimizationLocators.optimise_by_label, "", True,
                                        OptimizationLocators.optimise_by_operator_dropdown_item_value)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_operator_dropdown_item_value,
                                                     is_play=True, group_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_operator_dropdown_item_value,
                                                                       "pause", group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_operator_dropdown_item_value,
                                                     is_play=False, single_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_operator_dropdown_item_value,
                                                                       "play", group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_operator_dropdown_item_value,
                                                     is_play=True, group_action=True)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_operator_dropdown_item_value,
                                                     is_play=True, bulk_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_operator_dropdown_item_value,
                                                                       "pause", bulk_action=True)

        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_operator_dropdown_item_value,
                                                     is_play=False, group_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_operator_dropdown_item_value,
                                                                       "play", group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_operator_dropdown_item_value,
                                                     is_play=True, single_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_operator_dropdown_item_value,
                                                                       "pause", group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_operator_dropdown_item_value,
                                                     is_play=True, group_action=True)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_operator_dropdown_item_value,
                                                     is_play=False, bulk_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_operator_dropdown_item_value,
                                                                       "play", bulk_action=True)
        # [END] OPTIMISE BY OPERATOR

        # [START] OPTIMISE BY APP/SITE NAME
        base_page.select_dropdown_value(OptimizationLocators.optimise_by_label, "", True,
                                        OptimizationLocators.optimise_by_app_site_name_dropdown_item_value)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        base_page.wait_for_visibility_of_element(OptimizationLocators.app_site_column_locator,
                                                 time_out=base_page.ONE_MINUTE)
        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_app_site_name_dropdown_item_value,
                                                     is_play=True, group_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_app_site_name_dropdown_item_value,
                                                                       "pause", group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_app_site_name_dropdown_item_value,
                                                     is_play=False, single_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_app_site_name_dropdown_item_value,
                                                                       "play", group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_app_site_name_dropdown_item_value,
                                                     is_play=True, group_action=True)
        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_app_site_name_dropdown_item_value,
                                                     is_play=True, bulk_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_app_site_name_dropdown_item_value,
                                                                       "pause", bulk_action=True)

        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_app_site_name_dropdown_item_value,
                                                     is_play=False, group_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_app_site_name_dropdown_item_value,
                                                                       "play", group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_app_site_name_dropdown_item_value,
                                                     is_play=True, single_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_app_site_name_dropdown_item_value,
                                                                       "pause", group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_app_site_name_dropdown_item_value,
                                                     is_play=True, group_action=True)
        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_app_site_name_dropdown_item_value,
                                                     is_play=False, bulk_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_app_site_name_dropdown_item_value,
                                                                       "play", bulk_action=True)
        # [END] OPTIMISE BY APP/SITE NAME

        # [START] OPTIMISE BY PACKAGE
        base_page.select_dropdown_value(OptimizationLocators.optimise_by_label, "", True,
                                        OptimizationLocators.optimise_by_package_dropdown_item_value)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_package_dropdown_item_value,
                                                     is_play=True, group_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_package_dropdown_item_value,
                                                                       "pause", group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_package_dropdown_item_value,
                                                     is_play=False, single_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_package_dropdown_item_value,
                                                                       "play", group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_package_dropdown_item_value,
                                                     is_play=True, group_action=True)
        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_package_dropdown_item_value,
                                                     is_play=True, bulk_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_package_dropdown_item_value,
                                                                       "pause", bulk_action=True)

        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_package_dropdown_item_value,
                                                     is_play=False, group_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_package_dropdown_item_value,
                                                                       "play", group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_package_dropdown_item_value,
                                                     is_play=True, single_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_package_dropdown_item_value,
                                                                       "pause", group_and_single_action=True)
        optimization_page.click_on_play_pause_button("1", OptimizationLocators.optimise_by_package_dropdown_item_value,
                                                     is_play=True, group_action=True)
        optimization_page.click_on_play_pause_button("1",
                                                     OptimizationLocators.optimise_by_package_dropdown_item_value,
                                                     is_play=False, bulk_action=True)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        assert optimization_page.get_specific_play_pause_button_status("1",
                                                                       OptimizationLocators.optimise_by_package_dropdown_item_value,
                                                                      "play", bulk_action=True)
        # [END] OPTIMISE BY PACKAGE

        # [START] OPTIMISE BY PLACEMENT
        base_page.select_dropdown_value(OptimizationLocators.optimise_by_label, "", True,
                                        OptimizationLocators.optimise_by_placement_dropdown_item_value)
        base_page.click_on_element(OptimizationLocators.search_button_locator)
        if base_page.is_element_present(OptimizationLocators.grid_locator, base_page.FIVE_SEC_DELAY):
            optimization_page.click_on_play_pause_button("1",
                                                         OptimizationLocators.optimise_by_placement_dropdown_item_value,
                                                         is_play=True, group_action=True)
            base_page.click_on_element(OptimizationLocators.search_button_locator)
            assert optimization_page.get_specific_play_pause_button_status("1",
                                                                           OptimizationLocators.optimise_by_placement_dropdown_item_value,
                                                                           "pause", group_and_single_action=True)
            optimization_page.click_on_play_pause_button("1",
                                                         OptimizationLocators.optimise_by_placement_dropdown_item_value,
                                                         is_play=False, single_action=True)
            base_page.click_on_element(OptimizationLocators.search_button_locator)
            assert optimization_page.get_specific_play_pause_button_status("1",
                                                                           OptimizationLocators.optimise_by_placement_dropdown_item_value,
                                                                           "play", group_and_single_action=True)
            optimization_page.click_on_play_pause_button("1",
                                                         OptimizationLocators.optimise_by_placement_dropdown_item_value,
                                                         is_play=True, group_action=True)
            optimization_page.click_on_play_pause_button("1",
                                                         OptimizationLocators.optimise_by_placement_dropdown_item_value,
                                                         is_play=True, bulk_action=True)
            base_page.click_on_element(OptimizationLocators.search_button_locator)
            assert optimization_page.get_specific_play_pause_button_status("1",
                                                                           OptimizationLocators.optimise_by_placement_dropdown_item_value,
                                                                           "pause", bulk_action=True)

            optimization_page.click_on_play_pause_button("1",
                                                         OptimizationLocators.optimise_by_placement_dropdown_item_value,
                                                         is_play=False, group_action=True)
            base_page.click_on_element(OptimizationLocators.search_button_locator)
            assert optimization_page.get_specific_play_pause_button_status("1",
                                                                           OptimizationLocators.optimise_by_placement_dropdown_item_value,
                                                                           "play", group_and_single_action=True)
            optimization_page.click_on_play_pause_button("1",
                                                         OptimizationLocators.optimise_by_placement_dropdown_item_value,
                                                         is_play=True, single_action=True)
            base_page.click_on_element(OptimizationLocators.search_button_locator)
            assert optimization_page.get_specific_play_pause_button_status("1",
                                                                           OptimizationLocators.optimise_by_placement_dropdown_item_value,
                                                                           "pause", group_and_single_action=True)
            optimization_page.click_on_play_pause_button("1",
                                                         OptimizationLocators.optimise_by_placement_dropdown_item_value,
                                                         is_play=True, group_action=True)
            optimization_page.click_on_play_pause_button("1",
                                                         OptimizationLocators.optimise_by_placement_dropdown_item_value,
                                                         is_play=False, bulk_action=True)
            base_page.click_on_element(OptimizationLocators.search_button_locator)
            assert optimization_page.get_specific_play_pause_button_status("1",
                                                                           OptimizationLocators.optimise_by_placement_dropdown_item_value,
                                                                           "play", bulk_action=True)
        else:
            print("No data to perform optimisation")
        # [END] OPTIMISE BY PLACEMENT
