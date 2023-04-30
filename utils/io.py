import json
import os
import time
from configurations.mysql import get_mysql_client
from configurations import generic_modules
import datetime
import requests


class IoUtils:

    @staticmethod
    def pull_open_ios_from_db():
        attempts = 0
        db_result = None
        open_ios = []
        io_amounts = []
        while attempts < generic_modules.MYSQL_MAX_RETRY:
            try:
                time.sleep(generic_modules.MYSQL_WAIT_TIME)
                connection = get_mysql_client()
                with connection.cursor() as cursor:
                    sql_select_query = ' SELECT io.* FROM io io LEFT JOIN invoice_ios ii ON ii.io_id = io.id LEFT JOIN ' \
                                       'invoices i ON i.id = ii.invoice_id LEFT JOIN io_proforma ip ON ip.io_id = io.id' \
                                       ' WHERE i.invoice_number IS NULL AND ip.invoice_status NOT IN (1,4) AND ' \
                                       'io.company_id = 9718 AND (io.status != 1 OR io.status IS NULL) AND ' \
                                       'io.invoice_status NOT IN (4,1,6) AND io.io_number IS NOT NULL AND ip.paid = ' \
                                       '0 GROUP BY io.id'
                    cursor.execute(sql_select_query)
                    connection.commit()
                    db_results = cursor.fetchall()
                connection.close()
                for db_result in db_results:
                    db_result = dict(db_result)
                    db_result['io_number'] = float(db_result['io_number'])
                    db_result['total'] = db_result['total']
                    open_ios.append(db_result['io_number'])
                    io_amounts.append(db_result['total'])
                if db_result is None:
                    attempts += 1
                    continue
                else:
                    return open_ios, io_amounts
            except Exception as e:
                print("Error in DB Connection", e)
                try:
                    connection.close()
                except Exception as e:
                    print("Error in DB Connection Closing", e)
                attempts += 1
                continue
        return open_ios, io_amounts

    @staticmethod
    def pull_finance_balances_from_db():
        attempts = 0
        db_result = None
        balances = []
        while attempts < generic_modules.MYSQL_MAX_RETRY:
            try:
                time.sleep(generic_modules.MYSQL_WAIT_TIME)
                connection = get_mysql_client()
                with connection.cursor() as cursor:
                    sql_select_query = 'SELECT i.id, DATE_ADD(i.date, INTERVAL i.payment_term DAY) due_date, ' \
                                       'i.currency_rate, ipa.balance/i.currency_rate as balance FROM io `io` ' \
                                       'INNER JOIN invoice_ios ii ' \
                                       'ON ii.io_id = io.id INNER JOIN invoices i ON i.id = ii.invoice_id INNER ' \
                                       'JOIN users_admin ua ON `i`.client_id = ua.id LEFT JOIN invoice_campaigns ic ' \
                                       'ON `i`.id = ic.invoice_id LEFT JOIN io_proforma ip ON ip.io_id = io.id LEFT ' \
                                       'JOIN companies cou ON i.company_id = cou.id LEFT JOIN campaigns c ON ' \
                                       'ic.campaign_id = c.id LEFT JOIN currencies cu ON i.currency_id = cu.id ' \
                                       'LEFT JOIN company_profiles cp ON `i`.company_profile = cp.id LEFT JOIN ' \
                                       'company_profiles cp2 ON i.company_profile = cp2.id LEFT JOIN ' \
                                       'invoice_payment_log ipls ON ipls.id = i.id AND ipls.type = "invoice" LEFT ' \
                                       'JOIN invoice_proforma_aggregator ipa ON ipa.item_id = i.id AND ipa.type = ' \
                                       '"invoice" WHERE (io.status != 1 OR io.status IS NULL) AND (i.status != 1 OR ' \
                                       'i.status IS NULL) AND cou.id = 9718 AND i.invoice_number IS NOT NULL GROUP ' \
                                       'BY i.id UNION ALL SELECT ip.id, DATE_ADD(ip.date, INTERVAL ' \
                                       'ip.payment_term DAY) due_date, ip.currency_rate, ipa.balance FROM io ' \
                                       '`io` INNER JOIN io_proforma ip ON `io`.id = ip.io_id INNER JOIN ' \
                                       'users_admin ua ON `ip`.client_id = ua.id LEFT JOIN invoice_ios ii ' \
                                       'ON ii.io_id = io.id LEFT JOIN invoices i ON i.id = ii.invoice_id LEFT ' \
                                       'JOIN io_proforma_campaigns ic ON `ip`.id = ic.proforma_id LEFT JOIN ' \
                                       'companies cou ON ip.company_id = cou.id LEFT JOIN campaigns c ON ' \
                                       'ic.campaign_id = c.id LEFT JOIN currencies cu ON ip.currency_id = ' \
                                       'cu.id LEFT JOIN company_profiles cp ON `ip`.company_profile = ' \
                                       'cp.id LEFT JOIN company_profiles cp2 ON ip.company_profile = cp2.id ' \
                                       'LEFT JOIN invoice_payment_log ipls ON ipls.id = ip.id AND ipls.type = ' \
                                       '"proforma" LEFT JOIN invoice_proforma_aggregator ipa ON ipa.item_id = ' \
                                       'ip.id AND ipa.type = "proforma" WHERE ip.invoice_status IN (1,4) AND ' \
                                       '(i.status != 1 OR i.status IS NULL) AND (ip.status != 1 OR ' \
                                       'ip.status IS NULL) AND cou.id = 9718 AND i.invoice_number IS ' \
                                       'NULL GROUP BY ip.id ORDER BY `id` DESC'
                    cursor.execute(sql_select_query)
                    connection.commit()
                    db_results = cursor.fetchall()
                connection.close()
                for db_result in db_results:
                    db_result = dict(db_result)
                    db_result['balance'] = float(db_result['balance'])
                    balances.append(db_result['balance'])
                if db_result is None:
                    attempts += 1
                    continue
                else:
                    return balances
            except Exception as e:
                print("Error in DB Connection", e)
                try:
                    connection.close()
                except Exception as e:
                    print("Error in DB Connection Closing", e)
                attempts += 1
                continue
        return balances
