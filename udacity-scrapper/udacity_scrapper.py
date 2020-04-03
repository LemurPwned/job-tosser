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

                all_skills = card.findAll('span',
                                          {'class': 'ng-star-inserted'})
                skill_list = []
                for skill in all_skills:
                    skill_list.append(skill.text)
                if category:
                    category = category.text.strip()

                real_link = title.find('a', {'class': 'capitalize'})['href']
         
                db['course'].append(real_title)
                db['link'].append(real_link)
                db['desc'].append(skill_list[-1])
                db['skills'].append(skill_list[:-1])
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
