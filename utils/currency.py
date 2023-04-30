import time
from configurations.mysql import get_mysql_client
from configurations import generic_modules

connection = ''


class CurrencyUtils:

    @staticmethod
    def pull_currency_rate_data_db(currency_ids):
        global connection
        attempts = 0
        db_result = None
        currency_rates = []
        while attempts < generic_modules.MYSQL_MAX_RETRY:
            try:
                time.sleep(generic_modules.MYSQL_WAIT_TIME)
                connection = get_mysql_client()
                with connection.cursor() as cursor:
                    sql_select_query = 'SELECT currency_rate_usd, markup_amount FROM billing_currency_rates WHERE ' \
                                       'currency_id in (' + currency_ids + ') ORDER BY currency_id'
                    cursor.execute(sql_select_query)
                    connection.commit()
                    db_results = cursor.fetchall()
                connection.close()
                for db_result in db_results:
                    db_result = dict(db_result)
                    db_result['currency_rate_usd'] = float(db_result['currency_rate_usd'])
                    db_result['markup_amount'] = float(db_result['markup_amount'])
                    currency_rate_markup = (db_result['currency_rate_usd'] * db_result['markup_amount']) / 100
                    currency_rate = db_result['currency_rate_usd'] + currency_rate_markup
                    currency_rates.append(currency_rate)
                if db_result is None:
                    attempts += 1
                    continue
                else:
                    return currency_rates
            except Exception as e:
                print("Error in DB Connection", e)
                try:
                    connection.close()
                except Exception as e:
                    print("Error in DB Connection Closing", e)
                attempts += 1
                continue
        return currency_rates

    @staticmethod
    def pull_specific_currency_rate_data_db(currency_id):
        global connection
        attempts = 0
        db_result = None
        currency_rate = 0
        while attempts < generic_modules.MYSQL_MAX_RETRY:
            try:
                time.sleep(generic_modules.MYSQL_WAIT_TIME)
                connection = get_mysql_client()
                with connection.cursor() as cursor:
                    sql_select_query = 'SELECT currency_rate_usd, markup_amount FROM billing_currency_rates WHERE ' \
                                       'currency_id = ' + str(currency_id) + ''
                    cursor.execute(sql_select_query)
                    connection.commit()
                    db_results = cursor.fetchall()
                connection.close()
                for db_result in db_results:
                    db_result = dict(db_result)
                    db_result['currency_rate_usd'] = float(db_result['currency_rate_usd'])
                    db_result['markup_amount'] = float(db_result['markup_amount'])
                    currency_rate_markup = (db_result['currency_rate_usd'] * db_result['markup_amount']) / 100
                    currency_rate = db_result['currency_rate_usd'] + currency_rate_markup
                if db_result is None:
                    attempts += 1
                    continue
                else:
                    return currency_rate
            except Exception as e:
                print("Error in DB Connection", e)
                try:
                    connection.close()
                except Exception as e:
                    print("Error in DB Connection Closing", e)
                attempts += 1
                continue
        return currency_rate
