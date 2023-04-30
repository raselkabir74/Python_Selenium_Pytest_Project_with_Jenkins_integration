import json
import uuid
import requests
from configurations import configurations
from datetime import datetime

config = configurations.load_config_by_usertype()

BASE_URL = config['credential']['url']

username = config['credential']['username']
passphrase = config['credential']['password']

driver = None

step = 0

DELAY = 25

MYSQL_MAX_RETRY = int(config['mysql']['max-retry'])
MYSQL_WAIT_TIME = int(config['mysql']['wait'])
ONE_MINUTE_DELAY = int(config['wait']['one-minute'])
HALF_MINUTE_DELAY = int(config['wait']['half-minute'])
SHORT_DELAY = int(config['wait']['short-delay'])
FIVE_SEC_DELAY = int(config['wait']['five-sec-delay'])
ONE_SEC_DELAY = int(config['wait']['one-sec-delay'])


def get_api_access_token(base_url, end_point, credential):
    payload = {
        'grant_type': 'eskimi_dsp',
        'username': credential['username'],
        'password': credential['password'],
        'client_id': int(credential['client-id']),
        'client_secret': credential['client-secret']
    }
    headers = {'content-type': 'application/json'}
    response = json.loads(
        requests.request('POST', '{}{}'.format(base_url, end_point), data=json.dumps(payload), headers=headers).text)
    return response['access_token']


def get_random_string(length=10):
    return uuid.uuid4().hex[:length]


def step_printer(stepstr):
    global step
    if step == 0:
        step = step + 1
        print('\nStep {} --> {}'.format(step, stepstr))
    else:
        step = step + 1
        print('Step {} --> {}'.format(step, stepstr))

def step_info(info):
    print(info)

def ordered(obj):
    if isinstance(obj, dict):
        return sorted((k, ordered(v)) for k, v in obj.items())
    if isinstance(obj, list):
        return sorted(ordered(x) for x in obj)
    else:
        return obj


def time_within_range(start=6, end=10, x=int(datetime. now().strftime("%H"))):
    print(x)
    if start <= end:
        return start <= x <= end
    else:
        return start <= x or x <= end
