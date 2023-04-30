from configurations import generic_modules
from configurations.mysql import get_mysql_client
import time


class UserUtils:
    @staticmethod
    def get_bulk_user_url(user_email):
        try:
            time.sleep(generic_modules.MYSQL_WAIT_TIME)
            connection = get_mysql_client()
            with connection.cursor() as cursor:
                sql_select_query = "SELECT hash FROM bulk_user_create_invitation WHERE email = '{}';".format(user_email)
                cursor.execute(sql_select_query)
                connection.commit()
                db_result = cursor.fetchone()
            connection.close()
            url = generic_modules.BASE_URL + "/SignUp/createAccountFromInvite?verify_code=" + str(db_result['hash'])
            return url
        except Exception as e:
            print("Error in DB Connection", e)
            try:
                connection.close()
            except Exception as e:
                print("Error in DB Connection Closing", e)
