from collections import defaultdict
from bs4 import BeautifulSoup
import pandas as pd
import codecs
import os

class noFluffJobsParser():

    def __init__(self):
        self.results = []

        self.ens_data = {
            'Role':       [],
            'Tags' :      [],
            'Additional': [],
            'Salary': [],
            'Locations': []
        }

    def parse_data(self, data):
        bs = BeautifulSoup(data, 'html.parser')
        role = None
        try:
            role = bs.find("div", {"class": 'posting-details-description'}).find('h1').getText()
        except:
            print("No details")
            role = None
        tags = []
        additional = {}

        for aux in bs.findAll('nfj-posting-requirements'):
            for tag in aux.findAll('button'):
                tags += [tag.getText().replace('\n','')]

        search_elements = []
        try:
            search_elements = bs.find('nfj-posting-specs', {'id': 'posting-specs'}).findAll('div', {'class': 'row'})
        except:
            pass
        for aux in search_elements:

            title = aux.find('div', {'class', 'col-sm-6'})
            if title is not None:
                title = title.getText()

            value = aux.find('div', {'class', 'col-sm-6 value'})
            if value is not None:
                value = value.getText()

            additional[title] = value

        salary = None
        locations = None

        try:
            salary = bs.find('div', {'class': 'salary'}).find('h4').getText()
        except:
            salary = None
            print("no location found")

        try:
            locations = bs.find('li', {'class': 'text-break'}).getText()
        except:
            print("no salary found")
            salary = None
        
        #print(additional[title])
        

        return role, tags, additional, salary, locations

    def parse_files(self, filenames):
        for filename in filenames:
            if not filename.endswith('.html'):
                continue

            with open(filename, 'r', encoding = 'utf-8') as f:
                data = f.read()
                role, tags, additional, salary, locations = parser.parse_data(data)

                if tags:
                    self.ens_data['Role'] += [role]
                    self.ens_data['Tags'] += [tags]
                    self.ens_data['Additional'] += [additional]
                    self.ens_data['Salary'] += [salary]
                    self.ens_data['Locations'] += [locations]

if __name__ == '__main__':
    parser = noFluffJobsParser()

    ls = os.listdir('./noFluffJobs/websites')

    parser.parse_files(['./noFluffJobs/websites/' + dir for dir in ls])

    df = pd.DataFrame.from_dict(parser.ens_data)
    print(df.head())

    df.to_csv('no_fluffs.csv', index=False)



