from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from collections import defaultdict
import pandas as pd
import os
import requests


class UdacityScrapper:
    def __init__(self):
        self.data_save = './udacity-data/'

        os.makedirs(self.data_save, exist_ok=True)
        self.pages = 0

    def parse_course_list(self, link):

        db = defaultdict(list)
        res = requests.get(link)
        req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})

        with urlopen(req) as url_handl:
            html_code = url_handl.read()
            soup = BeautifulSoup(html_code, 'html.parser')

            with open(os.path.join(self.data_save, f'{self.pages}.html'),
                      'wb') as f:
                f.write(html_code)
            self.pages += 1

            course_cards = soup.findAll('div',
                                        {'class': 'course-summary-card'})
            for card in course_cards:
                title = card.find('h3', {'class': 'card-heading'})
                real_title = title.text
                category = card.find('h4', {'class': 'category'})

                course_level = card.find('span', {'class': 'level'})
                real_course_level = course_level.find('span',
                                                      {'class': 'capitalize'})

                skills_covered = card.find('div', {'class': 'skills'})
                if skills_covered:
                    all_skills = skills_covered.findAll(
                        'span', {'class': 'ng-star-inserted'})
                else: 
                    all_skills = None

                skill_list = []
                if all_skills:
                    for skill in all_skills:
                        skill_list.append(skill.text)
                    if category:
                        category = category.text.strip()

                real_link = title.find('a', {'class': 'capitalize'})['href']
                desc = card.find('div', {'class': 'card__expander'})
                real_desc = desc.find('span', {'class': 'ng-star-inserted'})
                if real_desc:
                    real_desc = real_desc.text
                db['course'].append(real_title)
                db['link'].append(real_link)
                db['desc'].append(real_desc)
                db['skills'].append(skill_list)
                db['category'].append(category)
                db['level'].append(real_course_level.text)

        df = pd.DataFrame.from_dict(db)
        df.to_csv(os.path.join(self.data_save, f'res.csv'), index=False)

    def run(self):
        url = r'https://www.udacity.com/courses/all'
        self.parse_course_list(url)


if __name__ == "__main__":

    us = UdacityScrapper()
    us.run()
