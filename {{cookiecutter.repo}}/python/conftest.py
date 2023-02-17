import logging

from selenium.webdriver.chrome.options import Options
import pytest

import {{cookiecutter.repo}}.server.app as app
# ------------------------------------------------------------------------------


def pytest_setup_options():
    '''
    Configures Chrome webdriver.
    '''
    options = Options()
    options.add_argument('--no-sandbox')
    return options


@pytest.fixture(scope='function')
def run_app():
    '''
    Pytest fixture used to run {{cookiecutter.repo}} Dash app.
    Sets config_path to resources/test_config.json.
    '''
    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    app.run(app.APP, CONFIG_PATH, debug=False, test=True)
    yield app.APP, app.APP.client
