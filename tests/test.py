"""
Test this.
"""
import requests
import unittest
import pytest
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from scripts.model_metrics import precision_recall_f1, get_auc_score

from app import application
from scripts import db


@pytest.fixture
def my_app():
    application.config['TESTING'] = True
    return application


@pytest.fixture
def driver():
    windows_driver = '/mnt/c/Users/kurtrm/Documents/bin/chromedriver.exe'
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--disable-gpu')
    browser = Chrome(executable_path=windows_driver,
                     chrome_options=options)
    return browser


def test_home_response(my_app):
    with my_app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200


def test_dummy_check(my_app):
    with my_app.test_client() as client:
        response = client.get('/fakeroute')
        assert response.status_code == 404


def test_home_content(my_app):
    with my_app.test_client() as client:
        response = client.get('/')
    html = response.get_data()
    soup = BeautifulSoup(html, 'html.parser')
    soup_auc = soup.find('div', {'id': 'auc'}).text
    soup_precision = soup.find('div', {'id': 'precision'}).text
    soup_recall = soup.find('div', {'id': 'recall'}).text
    soup_f1 = soup.find('div', {'id': 'f1'}).text
    auc = get_auc_score()
    precision, recall, f1, _ = precision_recall_f1()

    assert [float(value) for value in [soup_auc,
                                       soup_precision,
                                       soup_recall,
                                       soup_f1]] == [pytest.approx(auc, .1),
                                                     pytest.approx(precision, .1),
                                                     pytest.approx(recall, .1),
                                                     pytest.approx(f1, .1)]


def test_unit_analysis(my_app):
    """
    Test the unit analysis page.
    """
    with my_app.test_client() as client:
        response = client.get('/unit_analysis')
    assert response.status_code == 200
