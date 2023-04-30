from pages.sidebar.sidebar import DashboardSidebarPage
from pages.all_campaigns.all_campaigns_form import DashboardAllCampaignForm
from utils.compare import CompareUtils

def test_all_campaigns(login_by_user_type):
    config, driver = login_by_user_type
    sidebar_navigation = DashboardSidebarPage(driver)
    all_campaign_form = DashboardAllCampaignForm(driver)
    sidebar_navigation.navigate_to_all_campaigns()
    statuses = ['Pending', 'Live', 'Stopped', 'Daily cap', 'Budget limit', 'Ready', 'Expired', 'Rejected', 'Deleted',
                'Draft']
    type_names = ['Banner', 'Native', 'Video', 'Native video', 'Engagement', 'Carousel', 'Audio']
    expected_url_functions = ['optimisation', 'reporting', 'acampaigns', 'acampaigns', 'deletePending',
                              '1']
    assert all_campaign_form.all_statuses_verification(statuses)
    all_campaign_form.clear_all()
    assert all_campaign_form.user_filter_verification('AutomationAdminUser')
    all_campaign_form.clear_all()
    assert all_campaign_form.country_filter_verification('Bangladesh')
    all_campaign_form.clear_all()
    assert all_campaign_form.all_type_verification(type_names)
    all_campaign_form.clear_all()
    assert all_campaign_form.last_approved_by_verification('Arunas B.')
    all_campaign_form.clear_all()
    assert all_campaign_form.search_verification('Video Events Creative')
    all_campaign_form.clear_all()
    pulled_url_functions = all_campaign_form.verify_three_dot_options('AutomationAdminUser')
    assert 'All data verification is successful' == CompareUtils.verify_data(pulled_url_functions,
                                                                             expected_url_functions)
    all_campaign_form.clear_all()
