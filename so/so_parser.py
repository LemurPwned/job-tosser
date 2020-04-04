import urllib.request
from bs4 import BeautifulSoup
from lxml import html
import json
import pandas as pd
import requests
import os
import time
import re
from collections import defaultdict


class StackOverflowCarrers:
    def __init__(self, pages):
        self.main_url = 'https://stackoverflow.com/'
        self.pages = pages
        self.save_dir = 'data/soc'
        self.count = 1

    def download_job_specific(self, job_url, job_title):
        print(job_title)
        full_url = f"{self.main_url}{job_url}"
        with urllib.request.urlopen(full_url) as url_handl:
            html_code = url_handl.read().decode("utf-8")
            jb_title = job_title.replace(' ', '_')
            for sgn in ['?', '*', '!', ',', '-', '/', '\\', '(', ')']:
                jb_title = jb_title.replace(sgn, '')
            with open(os.path.join(self.save_dir, f"{self.count}_{jb_title}.html"),
                      'w') as f:
                f.write(html_code)
            self.count += 1

    def main_scrapper(self, timeout=0.2):
        rgx = re.compile(r".*")
        for i in range(self.pages):
            # https://stackoverflow.com/jobs?sort=i&pg=2
            url = f"{self.main_url}jobs?sort=i&pg={i}"
            print(url)
            with urllib.request.urlopen(url) as url_handl:
                html_code = url_handl.read()
                soup = BeautifulSoup(html_code, 'html.parser')
                jobs_on_page = soup.findAll("div", {"data-jobid": True})
                for job in jobs_on_page:
                    job_posting = job.find('a', {"class": 'job-link'})
                    job_id = job_posting['href'].split('/')  # take job id
                    try:
                        self.download_job_specific(job_url=f"jobs/{job_id[2]}",
                                                job_title=job_posting['title'])
                    except:
                        print("Parsing error! Skipping!")
                    time.sleep(timeout)

    def parse_job_posting(self, filename):
        metrics = {
            k: None
            for k in [
                'Job type', 'Experience level', 'Role', 'Industry',
                'Company size', 'Company type'
            ]
        }
        with open(filename, 'r') as f:
            html_text = f.read()
            soup = BeautifulSoup(html_text, 'html.parser')

            job_desc = soup.findAll('div', {'class': "mb8"})
            for desc in job_desc:
                desc_type = desc.find('span', {'class': False}).text.strip().replace(':', '')
                desc_content = desc.find('span', {'class': True}).text.strip().replace(':', '')
                if desc_type in metrics:
                    metrics[desc_type] = desc_content

            tags = [] 
            job_section = soup.findAll('section', {'class': 'mb32'})
            for section in job_section:
                subh2 = section.findAll('h2', {'class': "fs-subheading mb16"})
                for h2 in subh2:
                    if h2.text == 'Technologies':
                        job_tags = section.findAll('a', {"class": "post-tag job-link no-tag-menu"})
                        tags = [tag.text for tag in job_tags]
                        return tags, metrics
        
if __name__ == "__main__":
    soc = StackOverflowCarrers(10000)
    # soc.main_scrapper(2)
    print(
        soc.parse_job_posting(
            'data/stack_overflow_careers/Web_Developer.html'))
