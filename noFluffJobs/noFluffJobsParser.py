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
            'Additional': []
        }

    def parse_data(self, data):
        bs = BeautifulSoup(data, 'html.parser')
        role = bs.find('nfj-posting-header', {'id': 'posting-header'}).find('h1').getText()
        tags = []
        additional = {}

        for aux in bs.findAll('nfj-posting-requirements'):
            for tag in aux.findAll('button'):
                tags += [tag.getText().replace('\n','')]

        for aux in bs.find('nfj-posting-specs', {'id': 'posting-specs'}).findAll('div', {'class': 'row'}):

            title = aux.find('div', {'class', 'col-sm-6'})
            if title is not None:
                title = title.getText()

            value = aux.find('div', {'class', 'col-sm-6 value'})
            if value is not None:
                value = value.getText()

            additional[title] = value

        return role, tags, additional

    def parse_files(self, filenames):
        for filename in filenames:
            if not filename.endswith('.html'):
                continue

            with open(filename, 'r', encoding = 'utf-8') as f:
                data = f.read()
                role, tags, additional = parser.parse_data(data)

                if tags:
                    self.ens_data['Role'] += [role]
                    self.ens_data['Tags'] += [tags]
                    self.ens_data['Additional'] += [additional]

if __name__ == '__main__':
    parser = noFluffJobsParser()

    ls = os.listdir('noFluffJobs/websites')

    parser.parse_files(['./noFluffJobs/websites/' + dir for dir in ls])

    df = pd.DataFrame.from_dict(parser.ens_data)

    df.to_csv('no_fluffs.csv')



