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
from tqdm import tqdm
import pickle


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
                    job_posting = job.find('a', {"class": 's-link stretched-link'})
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
                'Company size', 'Company type', 'Salary', 'Remote', 
                'Location'
            ]
        }
        with open(filename, 'r') as f:
            html_text = f.read()
            soup = BeautifulSoup(html_text, 'html.parser')
            main_bar = soup.find('div', {'id': 'mainbar'})
            grid_cell = main_bar.find('div', {'class': 'grid--cell fl1 sm:mb12'})
            location = grid_cell.find('span', {'fc-black-500'}).text.replace(" ", "").replace("\n", "")[1:]
            
            mt12 = main_bar.find('div', {'class': 'mt12'})
            salary = None
            remote = None
            try:
                salary = mt12.find('span', {'class': '-salary pr16'})['title']
            except:
                pass

            try:
                remote = mt12.find('span', {'class': '-remote pr16'}).text.replace(" ", "").replace("\n", "")
            except:
                pass
            
            metrics["Location"] = location
            metrics["Salary"] = salary
            metrics["Remote"] = remote
            doc = soup.find('div', {"id": "overview-items"})
            doc = soup.findAll('section', {'class': 'mb32'})
            #print(doc)
            job_desc = doc[0].findAll('div', {'class': "mb8"})
            for desc in job_desc:
                #print(desc)
                desc_type = desc.find('span', {'class': False}).text.strip().replace(':', '')
                desc_content = desc.find('span', {'class': True}).text.strip().replace(':', '')
                if desc_type in metrics:
                    metrics[desc_type] = desc_content

            #print(metrics)
            tags = [] 
            technologies = doc[1]
            job_tags = technologies.findAll('a', {"class": "post-tag no-tag-menu"})
            tags = [tag.text for tag in job_tags]
            return tags, metrics
     

   

if __name__ == "__main__":
    soc = StackOverflowCarrers(10000)
    #soc.main_scrapper(2)
    data = []
    ls = os.listdir('./data/soc/')
     
    i = 0
    for f in tqdm(ls):
        #f = "1668_Mid_to_Senior_Front_End_Developer__$75K_to_$110000__LOCALREMOTE.html"
        #print(f)
        data.append((soc.parse_job_posting("./data/soc/" + f)))
        #time.sleep(1)
        #break
    #print(data)
    pickle.dump(data, open("so.pkl", "wb"))
    
