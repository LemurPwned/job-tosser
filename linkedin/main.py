from selenium import webdriver
from client import LIClient
import argparse
import time
import random


if __name__ == "__main__":

    # initialize selenium webdriver - pass latest chromedriver path to webdriver.Chrome()
    #driver = webdriver.Chrome('/usr/local/bin/chromedriver')
    options = webdriver.ChromeOptions()
    options.add_argument("--headless")
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    driver = webdriver.Remote(
        command_executor="http://172.17.0.3:4445/wd/hub",
        desired_capabilities=options.to_capabilities()
    )

    #driver.maximize_window()
    driver.get("https://www.linkedin.com/uas/login")

    # initialize LinkedIn web client
    liclient = LIClient(driver, username='jan.kowali.69.69.69@gmail.com', password='aladarlinked1000')

    liclient.login()

    # wait for page load
    time.sleep(1 + random.gauss(2, 1))
    liclient.navigate_to_jobs_page()
    liclient.go_to_search_page()
    liclient.navigate_get_search_results()
    liclient.driver_quit()
