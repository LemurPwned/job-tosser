from __future__ import print_function
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import datetime
import json
import time
from itertools import zip_longest
from settings import search_keys, cities
import random



def write_line_to_file(filename, data):
    with open(filename, 'a', encoding='utf-8') as f:
        for line in data:
            json.dump(line, f, ensure_ascii=False, indent=4)

def get_date_time():
    """
    get the full date along with the hour of the search, just for 
    completeness. Allows us to solve for of the original post 
    date.
    """
    now   =  datetime.datetime.now()
    month =  str(now.month) if now.month > 9 else '0' + str(now.month)
    day   =  str(now.day) if now.day > 9 else '0' + str(now.day)
    date  =  ''.join(str(t) for t in [now.year, month, day, now.time().hour])
    return date

def adjust_date_range(driver, date_range):
    """select a specific date range for job postings"""
    if date_range == 'All':
        return
    index = ['', 'All', '1', '2-7', '8-14', '15-30'].index(date_range)
    button_path = "html/body/div[3]/div/div[2]/div[1]/div[4]/form/div/ul/li" \
                  "[3]/fieldset/button"
    date_path = "html/body/div[3]/div/div[2]/div[1]/div[4]/form/div/ul/li" \
                "[3]/fieldset/div/ol/li[{}]/div/label".format(index)
    attempts = 1
    while True:
        try:
            elem = driver.find_element_by_xpath(button_path)
            time.sleep(3)
        except Exception as e:
            attempts += 1
            if attempts > 25:
                break
        else:
            elem.click()
            time.sleep(3)
            driver.find_element_by_xpath(date_path).click()
            time.sleep(3)
            break 

def adjust_search_radius(driver, search_radius):
    """
    select the appropriate user-defined search radius from the 
    dropdown window
    """
    if search_radius == '50':
        return
    distance_selector = "select#advs-distance > option[value='{}']"
    distance_selector = distance_selector.format(search_radius)
    try:
        driver.find_element_by_css_selector(distance_selector).click()
    except Exception as e:
        print(e)
    else:
        time.sleep(3)
        try:
            driver.find_element_by_css_selector("input.submit-advs").click()
            time.sleep(3)
        except Exception as e:
            print(e)

def adjust_salary_range(driver, salary):
    """adjust the salary range, default is All salaries"""
    if salary == 'All': 
        return
    index = ['', 'All', '40+', '60+', '80+', '100+', 
                        '120+', '160+', '180+', '200+'].index(salary)
    salary_button = "html/body/div[3]/div/div[2]/div[1]/div[4]/form/div/ul/" \
                                    "li[4]/fieldset/button"
    salary_path = "html/body/div[3]/div/div[2]/div[1]/div[4]/" \
                  "form/div/ul/li[4]/fieldset/div[1]/ol/li[{}" \
                  "]/div/label".format(index)
    attempts = 1
    while True:
        try:
            elem = driver.find_element_by_xpath(salary_button)
            time.sleep(3 + random.gauss(2, 1))
        except Exception as e:
            attempts += 1
            if attempts > 25: 
                break
        else:
            elem.click()
            time.sleep(3 + random.gauss(2,1))
            driver.find_element_by_xpath(salary_path).click()
            break

def sort_results_by(driver, sorting_criteria):
    """sort results by either relevance or date posted"""
    if sorting_criteria.lower() == 'relevance':
        return
    button = '//select[@id="jserp-sort-select"]'
    option_path = '//option[@value="DD"]'
    time.sleep(3)
    try:
        driver.find_element_by_xpath(button).click()
    except Exception as e:
        print(e)
        print("  Could not sort results by '{}'".format(sorting_criteria))
    else:
        time.sleep(3)
        try:
            driver.find_element_by_xpath(option_path).click()
        except Exception as e:
            print("  Could not select 'sort by' option")
        else:
            time.sleep(3 + random.gauss(2, 1))

def robust_wait_for_clickable_element(driver, delay, selector):
    """ wait for css selector to load """
    clickable = False
    attempts = 1
    try:
        driver.find_element_by_xpath(selector)
    except Exception as e:
        print("  Selector not found: {}".format(selector))
    else:
        while not clickable:
            try:
                time.sleep(1 + random.gauss(2, 1))
                # wait for job post link to load
                wait_for_clickable_element(driver, delay, selector)
            except Exception as e:
                print("  {}".format(e))
                attempts += 1
                if attempts % 100 == 0:
                    driver.refresh()
                if attempts > 10**3: 
                    print("  \nrobust_wait_for_clickable_element failed " \
                                    "after too many attempts\n")
                    break
                pass
            else:
                clickable = True

def robust_click(driver, delay, selector):
    """
    use a while-looop to click an element. For stubborn links
    and general unexpected browser errors.
    """
    try:
        driver.find_element_by_xpath(selector).click()
    except Exception as e:
        print("  The job post link was likely hidden,\n    An " \
                "error was encountered while attempting to click link" \
                "\n    {}".format(e))
        attempts = 1
        clicked = False
        while not clicked:
            time.sleep(1 + random.gauss(2, 1))
            try:
                driver.find_element_by_xpath(selector).click()
            except Exception as e:
                pass
            else:
                clicked = True
                print("  Successfully navigated to job post page "\
                            "after {} attempts".format(attempts))
            finally:
                attempts += 1
                if attempts % 100 == 0:
                    print("--------------  refreshing page")
                    driver.refresh()
                    time.sleep(5)
                if attempts > 10**3:
                    print(selector)
                    print("  robust_click method failed after too many attempts")
                    break 


def wait_for_clickable_element(driver, delay, selector):
    """use WebDriverWait to wait for an element to become clickable"""
    obj = WebDriverWait(driver, delay).until(
            EC.element_to_be_clickable(
                (By.XPATH, selector)
            )
        )
    return obj  

def wait_for_clickable_element_css(driver, delay, selector):
    """use WebDriverWait to wait for an element to become clickable"""
    obj = WebDriverWait(driver, delay).until(
            EC.element_to_be_clickable(
                (By.CSS_SELECTOR, selector)
            )
        )
    return obj  


def link_is_present(driver, delay, selector, index, results_page):
    """
    verify that the link selector is present and print the search 
    details to console. This method is particularly useful for catching
    the last link on the last page of search results
    """
    try:
        WebDriverWait(driver, delay).until(
            EC.presence_of_element_located(
                (By.XPATH, selector)
            )
        )
        print("**************************************************")
        print("\nScraping data for result  {}" \
                "  on results page  {} \n".format(index, results_page))
    except Exception as e:
        print(e)
        if index < 25:
            print("\nWas not able to wait for job_selector to load. Search " \
                    "results may have been exhausted.")
            return True
        else:
            return False
    else:
        return True 


def search_suggestion_box_is_present(driver, selector, index, results_page):
    """
    check results page for the search suggestion box,
    as this causes some errors in navigate search results.
    """
    if (index == 1) and (results_page == 1):
        try:
            # This try-except statement allows us to avoid the 
            # problems cause by the LinkedIn search suggestion box
            driver.find_element_by_css_selector("div.suggested-search.bd")
        except Exception as e:
            pass
        else:
            return True
    else:
        return False

def next_results_page(driver, delay):
    """
    navigate to the next page of search results. If an error is encountered
    then the process ends or new search criteria are entered as the current 
    search results may have been exhausted.
    """
    try:
        # wait for the next page button to load
        print("  Moving to the next page of search results... \n" \
                "  If search results are exhausted, will wait {} seconds " \
                "then either execute new search or quit".format(delay))
        wait_for_clickable_element_css(driver, delay, "a.next-btn")
        # navigate to next page
        driver.find_element_by_css_selector("a.next-btn").click()
    except Exception as e:
        print ("\nFailed to click next page link; Search results " \
                                "may have been exhausted\n{}".format(e))
        raise ValueError("Next page link not detected; search results exhausted")
    else:
        # wait until the first job post button has loaded
        first_job_button = "a.job-title-link"
        # wait for the first job post button to load
        wait_for_clickable_element_css(driver, delay, first_job_button)

def print_num_search_results(driver,):
    """print the number of search results to console"""
    # scroll to top of page so first result is in view
    driver.execute_script("window.scrollTo(0, 0);")
    selector = "/html/body/div[6]/div[4]/div[3]/section[1]/div[2]/div/div/div[1]/div[1]/h1/small"
    try:
        num_results = driver.find_element_by_xpath(selector).text
    except Exception as e:
        num_results = ''
    print("**************************************************")
    print("\n\n\n\n\nSearching  {} " \
            "\n\n\n\n\n".format(num_results))


def grouper(iterable, n):
    "Collect data into fixed-length chunks or blocks"
    # grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    args = [iter(iterable)] * n
    return zip(*args)

class LIClient(object):
    def __init__(self, driver, **kwargs):
        self.driver         =  driver
        self.username       =  kwargs["username"]
        self.password       =  kwargs["password"]
        self.filename       =  search_keys["filename"]

    def driver_quit(self):
        self.driver.quit()

    def login(self):
        """login to linkedin then wait 3 seconds for page to load"""
        # Enter login credentials
        WebDriverWait(self.driver, 120).until(
            EC.element_to_be_clickable(
                (By.ID, "username")
            )
        )
        elem = self.driver.find_element_by_id("username")
        elem.send_keys(self.username)
        elem = self.driver.find_element_by_id("password")
        elem.send_keys(self.password)
        # Enter credentials with Keys.RETURN
        elem.send_keys(Keys.RETURN)
        # Wait bo tak
        time.sleep(1 + random.gauss(2, 1))

    def navigate_to_jobs_page(self):
        """
        Dont look here. I stole it.
        """
        # Click the Jobs search page
        jobs_link_clickable = False
        attempts = 1
        url = "https://www.linkedin.com/jobs/?trk=nav_responsive_sub_nav_jobs"
        while not jobs_link_clickable:
            time.sleep(random.randint(1, 3))
            try:
                self.driver.get(url)
            except Exception as e:
                attempts += 1
                if attempts > 10**3: 
                    print("  jobs page not detected")
                    break
                pass
            else:
                print("**************************************************")
                print ("\n\n\nSuccessfully navigated to jobs search page\n\n\n")
                jobs_link_clickable = True

    def go_to_search_page(self):
        """ GO TO MFKING SEARCH PAGE!"""

        driver = self.driver
        time.sleep(1 + random.gauss(2, 1))
        elem = driver.find_element_by_class_name("jobs-search-box__submit-button")
        elem.send_keys(Keys.ENTER)
        time.sleep(1 + random.gauss(2, 1))

    def navigate_get_search_results(self):
        """
        scrape postings for all pages in search results
        """
        driver = self.driver
        print_num_search_results(driver)

        # wait bo tak
        time.sleep(1 + random.gauss(2, 1))

        print('driver.find_elements_by_class_name()', len(driver.find_elements_by_class_name('occludable-update')))

        # spac mi sie chce, ok? i tak w koncu spadnie z rowerka
        import copy
        current_url = copy.deepcopy(self.driver.current_url)

        for city in cities:
            data = []
            print('city', city)
            i = 0
            if city == "USA":
                i=7
            while True:
                print('iiiiiiiii', i)

                self.driver.get(f'{current_url}?location={city}&start={i * 25}')
                time.sleep(1 + random.gauss(2, 1))

                for idx, item in enumerate(driver.find_elements_by_class_name('occludable-update')):
                    print('number on this page', idx)
                    #item = item.find_element_by_class_name('job-card-search__title')
                    item.click()
                    time.sleep(random.randint(1, 3))

                    try:
                        position = driver.find_element_by_class_name('jobs-details-top-card__job-title').text
                    except:
                        print('died RIP')
                        i += 1
                        break

                    # good luck parsing that
                    # this motherfucker is pure up to recruiter
                    # usually they make headers bold, BUT not always, fuq :<
                    # whole_fuqing_unnormalized_bastard_body = driver.find_element_by_css_selector('#job-details > span').get_attribute('innerHTML')
                    # just changed my mind bout naming...

                    whole_unnormalized_body = driver.find_element_by_css_selector('#job-details > span').get_attribute('innerHTML')
                    item_data = {
                        'position': position,
                        'whole_unnormalized_body': whole_unnormalized_body,
                        'job_description_details': {}
                    }

                    header_info = driver.find_element_by_css_selector('.jobs-details-top-card__company-info').text
                    groups = grouper(header_info.splitlines(), 2)
                    for header, content in groups:
                        item_data[header] = content

                    job_description_details = driver.find_element_by_class_name('jobs-description-details')
                    for job_description_item in job_description_details.find_elements_by_class_name('jobs-box__group'):
                        header, content = job_description_item.text.splitlines()
                        item_data['job_description_details'][header] = content

                    data.append(item_data)

                # write to file
                write_line_to_file(f'{city}.txt', data)
                data = []
                i += 1

                # looks like max
                if i > 39:
                    break
