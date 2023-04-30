import json
import os
import time
from configurations.mysql import get_mysql_client
from configurations import generic_modules
import datetime
import requests


class CampaignUtils:

    @staticmethod
    def pull_campaign_data_db(campaign_name):
        attempts = 0
        db_result = None
        while attempts < generic_modules.MYSQL_MAX_RETRY:
            try:
                time.sleep(generic_modules.MYSQL_WAIT_TIME)
                connection = get_mysql_client()
                with connection.cursor() as cursor:
                    sql_select_query = 'SELECT user_id, platform_id, ad_domain, click_url, country, bid_currency, ' \
                                       'budget_daily_currency, budget_total_currency, targeting, ' \
                                       'capping FROM campaigns where name = \'{}\' and user_id = 7722 ' \
                                       'and status = 0'.format(campaign_name)
                    cursor.execute(sql_select_query)
                    connection.commit()
                    db_result = cursor.fetchone()
                connection.close()
                db_result = dict(db_result)
                db_result['bid_currency'] = float(db_result['bid_currency'])
                db_result['budget_daily_currency'] = float(db_result['budget_daily_currency'])
                db_result['budget_total_currency'] = float(db_result['budget_total_currency'])
                db_result['targeting'] = json.loads(db_result['targeting'])
                del db_result['targeting']['date_from']
                del db_result['targeting']['date_to']
                del db_result['targeting']['excluded_operators']
                db_result['capping'] = json.loads(db_result['capping'])
                if db_result is None:
                    attempts += 1
                    continue
                else:
                    return db_result
            except Exception as e:
                print("Error in DB Connection", e)
                try:
                    connection.close()
                except Exception as e:
                    print("Error in DB Connection Closing", e)
                attempts += 1
                continue
        return db_result

    @staticmethod
    def create_campaign_by_api(config, user_type="admin", mass_campaign_name=""):
        access_token = generic_modules.get_api_access_token(config['credential']['api-url'], config['api']['oauth'],
                                                            config['credential'])
        api_url = '{}{}{}'.format(config['credential']['api-url'], config['api']['v1'], config['api']['banner-create'])
        with open('assets/campaign/campaign_data_api.json') as campaign_data:
            campaign_data = json.load(campaign_data)
        campaign_data['dates']['from'] = str(datetime.date.today() + + datetime.timedelta(days=2))
        campaign_data['dates']['to'] = str(datetime.date.today() + datetime.timedelta(days=7))
        if mass_campaign_name != "":
            campaign_data['name'] = mass_campaign_name
        else:
            campaign_data['name'] = campaign_data['name'] + generic_modules.get_random_string(5)
        campaign_data['userId'] = int(config['credential']['user-id'])
        campaign_data['creativeSetIds'] = [int(config['banner-creative-set-by-user-type'][user_type])]
        headers = {
            'content-type': 'application/json',
            'authorization': 'Bearer ' + access_token
        }
        response = json.loads(requests.request('POST', api_url, data=json.dumps(campaign_data), headers=headers).text)
        campaign = {
            'campaignId': response['id'],
            'name': campaign_data['name']
        }
        return campaign

    @staticmethod
    def process_campaign_approve_data(campaign_approve_data, single_approve=False):
        if single_approve:
            if campaign_approve_data['reporting_and_budget']['email_report']['is_checked'] == "False":
                campaign_approve_data['reporting_and_budget']['email_report']['is_checked'] = ""

            if campaign_approve_data['reporting_and_budget']['group_by_io']['is_checked'] == "False":
                campaign_approve_data['reporting_and_budget']['group_by_io']['is_checked'] = ""

            if campaign_approve_data['reporting_and_budget']['email_attachment']['xls']['is_checked'] == "False":
                campaign_approve_data['reporting_and_budget']['email_attachment']['xls']['is_checked'] = ""

            if campaign_approve_data['reporting_and_budget']['email_attachment']['pdf']['is_checked'] == "False":
                campaign_approve_data['reporting_and_budget']['email_attachment']['pdf']['is_checked'] = ""

            if campaign_approve_data['optimization_and_tracking']['campaign_run_on_eskimi']['is_checked'] == "False":
                campaign_approve_data['optimization_and_tracking']['campaign_run_on_eskimi']['is_checked'] = ""

        if campaign_approve_data['reporting_and_budget']['daily_budget_recalculation'] == "False":
            campaign_approve_data['reporting_and_budget']['daily_budget_recalculation'] = ""

        if campaign_approve_data['optimization_and_tracking']['strict_size_placement_size'] == "False":
            campaign_approve_data['optimization_and_tracking']['strict_size_placement_size'] = ""

        if campaign_approve_data['optimization_and_tracking']['multiple_bids_per_second'] == "False":
            campaign_approve_data['optimization_and_tracking']['multiple_bids_per_second'] = ""

        if campaign_approve_data['ad_exchange']['eskimi_margin'] == "False":
            campaign_approve_data['ad_exchange']['eskimi_margin'] = ""

        return campaign_approve_data

    @staticmethod
    def process_campaign_name(campaign_list, operation="mass approve"):
        debug_mode = "JENKINS_URL" not in os.environ
        if operation == "mass approve":
            if debug_mode:
                campaign_name_list = [
                    campaign_list['campaign-name-for-mass-approve-1'] + generic_modules.get_random_string(5),
                    campaign_list['campaign-name-for-mass-approve-2'] + generic_modules.get_random_string(5),
                    campaign_list['campaign-name-for-mass-approve-3'] + generic_modules.get_random_string(5),
                    campaign_list['campaign-name-for-mass-approve-4'] + generic_modules.get_random_string(5),
                    campaign_list['campaign-name-for-mass-approve-5'] + generic_modules.get_random_string(5)
                ]
            else:
                campaign_name_list = [
                    campaign_list['campaign-name-for-mass-approve-1'] + generic_modules.get_random_string(5),
                    campaign_list['campaign-name-for-mass-approve-2'] + generic_modules.get_random_string(5)
                ]
            return campaign_name_list
        elif operation == "mass duplicate and edit":
            if debug_mode:
                campaign_name_list = [
                    campaign_list['campaign-name-for-mass-edit-and-duplicate-1'] + generic_modules.get_random_string(5),
                    campaign_list['campaign-name-for-mass-edit-and-duplicate-2'] + generic_modules.get_random_string(5),
                    campaign_list['campaign-name-for-mass-edit-and-duplicate-3'] + generic_modules.get_random_string(5),
                    campaign_list['campaign-name-for-mass-edit-and-duplicate-4'] + generic_modules.get_random_string(5),
                    campaign_list['campaign-name-for-mass-edit-and-duplicate-5'] + generic_modules.get_random_string(5)
                ]
            else:
                campaign_name_list = [
                    campaign_list['campaign-name-for-mass-edit-and-duplicate-1'] + generic_modules.get_random_string(5),
                    campaign_list['campaign-name-for-mass-edit-and-duplicate-2'] + generic_modules.get_random_string(5)
                ]
            return campaign_name_list
        elif operation == "before mass duplicate operation":
            if debug_mode:
                campaign_name_list = [
                    campaign_list['campaign-name-before-mass-edit-and-duplicate-1'],
                    campaign_list['campaign-name-before-mass-edit-and-duplicate-2'],
                    campaign_list['campaign-name-before-mass-edit-and-duplicate-3'],
                    campaign_list['campaign-name-before-mass-edit-and-duplicate-4'],
                    campaign_list['campaign-name-before-mass-edit-and-duplicate-5']
                ]
            else:
                campaign_name_list = [
                    campaign_list['campaign-name-before-mass-edit-and-duplicate-1'],
                    campaign_list['campaign-name-before-mass-edit-and-duplicate-2']
                ]
            return campaign_name_list



