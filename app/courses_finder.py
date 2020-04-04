import ast
import json
from collections import Counter, defaultdict

import pandas as pd


def filter_tags(str_tag_list):
    tag_list = ast.literal_eval(str_tag_list)
    return [x.strip() for x in tag_list]


class CoursesFinder:
    def __init__(self, data_location):
        self.data_location = data_location
        self.prepare_db()

    def prepare_db(self):
        self.df = pd.read_csv(self.data_location)
        self.df['skills'] = self.df['skills'].apply(filter_tags)
        self.build_reverse_dict()

    def build_reverse_dict(self):
        black_list = ["New", "Free", "beginner", "advanced", "intermediate"]
        self.skill_to_courses = defaultdict(list)
        for _, row in self.df.iterrows():
            for skill in list(row['skills'][:-1]):
                if skill not in black_list:
                    self.skill_to_courses[skill.replace(
                        ",", "").lower()].append(row['course'])

    def find_best_fitting(self, skills):
        meeting_reqs = []
        for skill in skills:
            meeting_reqs.extend(self.skill_to_courses[skill])
        print(meeting_reqs)
        c = Counter(meeting_reqs)

        course, coocs = c.most_common(1)
        return json.dumps({'course': course, 'coocs': coocs})

    def perform_search(self, skills):
        if isinstance(skills, str):
            course_name = self.skill_to_courses[skills.lower()][0]
            course = self.df[self.df['course'] == course_name].iloc[0]
            return course
        else:
            return self.find_best_fitting([s.lower() for s in skills])


if __name__ == "__main__":
    cf = CoursesFinder('../data/res.csv')
    print(cf.perform_search(['Python', 'Data Science']))
    #cf.prepare_db()
