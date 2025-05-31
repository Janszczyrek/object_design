import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
import requests
import time
from datetime import datetime, timedelta


BASE_URL = "http://localhost:3000"


def get_driver():
    options = webdriver.ChromeOptions()
    service = ChromeService(executable_path='/usr/bin/chromedriver')
    driver = webdriver.Chrome(service=service, options=options)
    driver.implicitly_wait(5)
    return driver


def create_custom_tender(driver, orderer, price, name, description, start_time, end_time=None):
    if end_time is None:
        end_time = (datetime.today()+timedelta(seconds=5)).strftime('%m-%d-%Y\t%I:%M:%S%p')
        
    driver.find_element(By.XPATH, "//a[@href='/tenders/new']").click()
    tender_orderer_input = driver.find_element(By.XPATH, "//input[@name='orderer']")
    tender_orderer_input.send_keys(orderer)
    tender_price_input = driver.find_element(By.XPATH, "//input[@name='max_price']")
    tender_price_input.send_keys(price)
    tender_name_input = driver.find_element(By.XPATH, "//input[@name='name']")
    tender_name_input.send_keys(name)
    tender_description_input = driver.find_element(By.XPATH, "//textarea[@name='description']")
    tender_description_input.send_keys(description)
    tender_start_time_input = driver.find_element(By.XPATH, "//input[@name='start_time']")
    tender_start_time_input.send_keys(start_time)
    tender_end_time_input = driver.find_element(By.XPATH, "//input[@name='end_time']")
    tender_end_time_input.send_keys(end_time)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()


class BaseTestCase(unittest.TestCase):
    def setUp(self):
        self.driver = get_driver()
        self.driver.get(BASE_URL)
        requests.delete(f"{BASE_URL}/tenders/")  # Clear tenders before each test
        requests.delete(f"{BASE_URL}/offers/")  # Clear offers before each test

    def tearDown(self):
        self.driver.quit()