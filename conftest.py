import pytest
import logging
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from frontend.methods.connection_electricity_meter_builder import ElectricityMeterConnectionBuilder
from pathlib import Path


def pytest_addoption(parser):
    parser.addoption('--browser', default='chrome')
    parser.addoption('--headless', action='store_true')
    parser.addoption('--log_level', default='INFO')
    parser.addoption('--com_port', default='COM5')


@pytest.fixture()
def connection_electricity_meter(browser, com_port):
    connection_meter = (ElectricityMeterConnectionBuilder(browser).with_rs_485(com_port)
                        .with_configurator_access()
                        .build())
    yield connection_meter
    connection_meter.disconnection()


@pytest.fixture(scope='session')
def com_port(request):
    return request.config.getoption('--com_port')


@pytest.fixture()
def browser(request):
    browser_name = request.config.getoption('browser')
    headless = request.config.getoption('headless')
    log_level = request.config.getoption('log_level')

    logger = logging.getLogger(request.node.name)
    logs = Path('logs')
    logs.mkdir(exist_ok=True)
    screenshot = Path('screenshot')
    screenshot.mkdir(exist_ok=True)

    file_handler = logging.FileHandler(f'logs/{request.node.name}.log', mode="w")
    file_handler.setFormatter(logging.Formatter('%(levelname)s: %(message)s'))
    logger.addHandler(file_handler)
    logger.setLevel(level=log_level)

    logger.info(f'===> Test start at {datetime.datetime.now()}')

    browser = None

    chrome_options = Options()
    chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
    chrome_options.add_argument('--log-level=3')

    if browser_name == 'chrome':
        if headless:
            chrome_options.add_argument('headless')
            chrome_options.add_argument('--no-sandbox')
        browser = webdriver.Chrome(options=chrome_options)
    elif browser_name == 'edge':
        browser = webdriver.Edge()
    elif browser_name == 'firefox':
        browser = webdriver.Firefox()
    else:
        raise ValueError(f'Браузер {browser_name} не поддерживается')

    browser.implicitly_wait(2)
    browser.set_window_size(1680, 1050)

    browser.log_level = log_level
    browser.logger = logger
    browser.test_name = request.node.name

    logger.info(f'Browser {browser_name} started')
    yield browser

    def fin():
        browser.quit()
        logger.info(f'===> Test finished at {datetime.datetime.now()}')

    request.addfinalizer(fin)
    return browser
