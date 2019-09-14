import pytest
from fixtura.application import Application
import jsonpickle
import json
import os.path
import importlib
from fixtura.db import DbFixture
import ftputil

fixture = None
target = None

def load_config(file):
    global target
    if target is None:
        config_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), file)
        with open(config_file) as f:
            target = json.load(f)
    return target

@pytest.fixture(scope='session')
def config(request):
    return load_config(request.config.getoption("--target"))

@pytest.fixture
def app(request, config):
    global fixture
    browser = request.config.getoption("--browser")
    if fixture is None or fixture.is_not_valid():
        fixture = Application(browser=browser, config= config)
#   fixture.session.ensure_login(username=config["webadmin"]["username"], password=config["webadmin"]["password"])
    return fixture

@pytest.fixture(scope='session')
def db(request, config):
    dbfixture = DbFixture(host = config['db']['host'], name = config['db']['name'],
                          user = config['db']['user'], password = config['db']['password'])
    def fin():
        dbfixture.destroy()
        request.addfinalizer(fin)
    return dbfixture

def install_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            remote.remove("config_inc.php.bak")
        if remote.path.isfile("config_inc.php"):
            remote.rename("config_inc.php", "config_inc.php.bak")
        remote.upload(os.path.join(os.path.dirname(__file__), "resources/config_inc.php"),"config_inc.php")

def restore_server_configuration(host, username, password):
    with ftputil.FTPHost(host, username, password) as remote:
        if remote.path.isfile("config_inc.php.bak"):
            if remote.path.isfile("config_inc.php"):
                remote.remove("config_inc.php")
            remote.rename("config_inc.php.bak", "config_inc.php")


"""
@pytest.fixture(scope='session', autouse = True)
def configure_server(request, config):
    install_server_configuration(host = config['ftp']['host'], username = config['ftp']['username'], password = config['ftp']['password'])
    def fin():
        restore_server_configuration(host = config['ftp']['host'], username = config['ftp']['username'], password = config['ftp']['password'])
    request.addfinalizer(fin)
"""

@pytest.fixture(scope='session',autouse = True)
def stop(request):
    def fin():
        fixture.session.ensure_logout()
        fixture.destroy()
    request.addfinalizer(fin)
    return fixture

def pytest_addoption(parser):
    parser.addoption("--browser", action = "store", default = "firefox")
    parser.addoption("--target", action = "store", default = "target.json")

def pytest_generate_tests(metafunc):
    for fixture in metafunc.fixturenames:
        if fixture.startswith("data_"):
            testdata = load_from_module(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids = [str(x) for x in testdata])
        elif fixture.startswith("json_"):
            testdata = load_form_json(fixture[5:])
            metafunc.parametrize(fixture, testdata, ids = [str(x) for x in testdata])

def load_from_module(module):
    return importlib.import_module("data.%s" % module).testdata

def load_form_json(file):
    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "data/%s.json" % file)) as f:
        return jsonpickle.decode(f.read())
