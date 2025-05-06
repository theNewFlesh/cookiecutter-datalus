{%- set cc = cookiecutter -%}
{%- set repo_ = (cc.repo | replace('-', '_')) -%}
import logging

from selenium.webdriver.chrome.options import Options
import pytest

import {{cc.repo}}.server.app as app

CONFIG_PATH = '/home/ubuntu/{{repo_}}/resources/test_config.yaml'
# ------------------------------------------------------------------------------


def pytest_configure():
    '''
    Configures Chrome webdriver.
    '''
    options = Options()
    options.add_argument('--no-sandbox')
    return options


@pytest.fixture(scope='function')
def run_app():
    '''
    Pytest fixture used to run {{cc.repo}} Dash app.
    Sets config_path to resources/test_config.json.
    '''
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    app.run(app.APP, CONFIG_PATH, debug=False, test=True)
    yield app.APP, app.APP.client
