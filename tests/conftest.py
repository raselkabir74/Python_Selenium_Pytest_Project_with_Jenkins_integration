import time

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from configurations import configurations
from pages.index.index import DspDashboardIndex


@pytest.fixture
def config(scope='session'):
    config = configurations.load_config_by_usertype()
    return config


@pytest.fixture
def driver(config):
    c_options = Options()
    c_options.add_argument('--headless')
    c_options.add_argument('--no-sandbox')
    c_options.add_argument('--disable-gpu')
    c_options.add_argument('--disable-dev-shm-usage')
    c_options.add_argument("--window-size=1920,1080")
    c_options.add_argument('ignore-certificate-errors')
    driver = webdriver.Remote(
        command_executor="http://localhost:4444/wd/hub",
        options = c_options
    )
    driver.implicitly_wait(int(config['wait']['implicit']))
    yield driver
    print('Exiting driver!')
    driver.quit()


@pytest.fixture
def login_by_user_type(request, driver, env='stage'):
    marker = request.node.get_closest_marker("fixt_data")
    if marker is None:
        config = configurations.load_config_by_usertype()
    else:
        config = configurations.load_config_by_usertype(marker.args[0])
    index_page = DspDashboardIndex(config, driver, env)
    start = time.time()
    index_page.login()
    print('LOGGED IN: {}s'.format(int(time.time() - start)))
    return config, driver
