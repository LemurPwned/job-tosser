from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium import webdriver
import re
import os
from os import path
import time
from pathlib import Path

class fluffScrapper():

    def __init__(self):

        self.offers = []
        self.categories = [
            'javascript',
            'java',
            'angular',
            '.net',
            'react',
            'sql',
            'python',
            'rest',
            'spring',
            'php',
            'node',
            'aws',
            'hibernate',
            'c++',
            'jquery',
            'scala',
            'selenium',
            'redux',
            'android',
            'symfony',
            'ruby',
            'django',
            'swift',
            'Spark',
            'c'
        ]

        self.options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        self.options.add_experimental_option("prefs", prefs)
        self.options.add_argument('headless')
        self.driver = webdriver.Chrome('./chromedriver.exe', options = self.options)

        self.driver.get('https://nofluffjobs.com/')

        self.driver.execute_script("arguments[0].click();", self.driver.find_element_by_xpath('//button[@data-cy="btnAcceptCookie"]'))

    def search(self, job):

        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'search-input')))
        except:
            pass

        self.driver.find_element_by_class_name('search-input').send_keys(job)
        self.driver.execute_script("arguments[0].click();", self.driver.find_element_by_xpath('//button[@data-cy="searchJobButton"]'))

    def get_page_links(self):

        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, 'list-item')))
        except:
            pass

        for offer in self.driver.find_elements_by_class_name('list-item'):
            self.offers += [offer.find_element_by_tag_name('a').get_attribute('href')]

    def next_page(self):

        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[text()="»"]')))
        except:
            pass

        self.driver.execute_script("arguments[0].click();", self.driver.find_element_by_xpath('//*[text()="»"]'))

    def first_page(self):

        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[text()=" 1 "]')))
        except:
            pass

        self.driver.execute_script("arguments[0].click();", self.driver.find_element_by_xpath('//*[text()=" 1 "]'))

    def on_last_tab(self):

        try:
            WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.XPATH, '//*[text()="»"]')))
        except:
            return True

        if self.driver.find_element_by_class_name('pagination').find_elements_by_tag_name('li')[-1].find_element_by_tag_name('a').get_attribute('tabindex') == '-1':
            return True
        return False

    def save_offers(self):

        Path('./noFluffJobs/websites').mkdir(parents = True, exist_ok = True)

        for offer in self.offers:

            offer_name = offer.split('/')[-1]

            if path.exists('./websites/' + offer_name + '.html'):
                print('./websites/' + offer_name + '.html' + ' exists, omitting...')
                continue

            self.driver.get(offer)

            try:
                WebDriverWait(self.driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'nfj-posting-requirements')))
            except:
                continue

            with open('./websites/'+ offer_name + '.html', 'w', encoding = 'utf-8') as f:
                f.write(self.driver.page_source)

if __name__ == '__main__':

    scrapper = fluffScrapper()

    for category in scrapper.categories:
        scrapper.search(category)

        scrapper.first_page()

        while not scrapper.on_last_tab():
            scrapper.get_page_links()
            scrapper.next_page()

    scrapper.save_offers()