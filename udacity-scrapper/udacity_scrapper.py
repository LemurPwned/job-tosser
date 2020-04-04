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
                    start_pos = category.find('>')
                    if start_pos >= 0:
                        stop_pos = category.find('<', beg=start_pos)
                        category = category[start_pos+1:stop_pos]

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

                full_course_url = r'https://www.udacity.com' + real_link
                print(full_course_url)
                req = Request(full_course_url, headers={'User-Agent': 'Mozilla/5.0'})
                with urlopen(req) as url_handl:
                    html_code = url_handl.read()
                    soup = BeautifulSoup(html_code, 'html.parser')

                    try:
                        course_meta_info = soup.find('ir-canonical-degree-info-columns').find('div').find('ul')
                        elements = course_meta_info.findAll('li')
                        db['estimated_time'].append( elements[0].find('h5').getText() + ", " + elements[0].find('p').getText() )
                        try:
                            db['prerequisites'].append( elements[2].find('h5').getText().replace('and', '') ) # Remove 'and' for more convenient parsing
                        except IndexError as e:
                            db['enroll_by'].append('-')
                            db['prerequisites'].append( elements[1].find('h5').getText().replace('and', '') ) # Remove 'and' for more convenient parsing
                        else:
                            db['enroll_by'].append( elements[1].find('h5').getText() )
                    except AttributeError as e:
                        # Handle another formats
                        details = soup.find('div', {'class': 'details__stats'})
                        if details != None:
                            db['estimated_time'].append( details.find('div').findAll('div', {'class': 'col'})[1].find('h5').getText() )
                            db['enroll_by'].append('-')
                            db['prerequisites'].append( soup.find('div', {'class': 'course-reqs--summary'}).getText() )
                        else:
                            db['estimated_time'].append( soup.find('div', {'class': 'details__overview__item ng-star-inserted'}).getText() )
                            db['enroll_by'].append('-')
                            db['prerequisites'].append('-')


        df = pd.DataFrame.from_dict(db)
        df.to_csv(os.path.join(self.data_save, f'res.csv'), index=False)

    def run(self):
        url = r'https://www.udacity.com/courses/all'
        self.parse_course_list(url)


if __name__ == "__main__":

    us = UdacityScrapper()
    us.run()
