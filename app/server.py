import json
import os
from ast import literal_eval

from flask import Flask, render_template, request
from flask_cors import CORS

from aggregator import Aggregator
from courses_finder import CoursesFinder
from reverse_search import ReverseSearch
from skill_matcher import SkillMatcher
from utils import get_experience_count_by_technologies

app = Flask(__name__)

CORS(app)

DATA_LOC = '../data'
INDEX_FILE = 'index.html'
KEPLER_FILE = 'kepler.gl.html'
COURSES_SUBPAGE = "courses.html"
CHARTS_SUBPAGE = "charts.html"

DATABASE = os.path.join(DATA_LOC, 'DATABASE.pkl')
COURSE_DATABASE = os.path.join(DATA_LOC, 'res.csv')

# aggregator = Aggregator(DATABASE)
# r_search = ReverseSearch(DATABASE)
skill_matcher = SkillMatcher(DATABASE.replace('.pkl', '.csv'))

courses_finder = CoursesFinder(COURSE_DATABASE)


@app.route('/')
def root():
    return render_template(INDEX_FILE)


@app.route('/courses', methods=['GET'])
def skill():
    skill = request.args['skill'].lower()
    courses = courses_finder.perform_search(skill, 6)
    return render_template(COURSES_SUBPAGE, courses=courses)

@app.route('/salaries', methods=['GET'])
def salaries():
    skills = request.args['skills'].lower()
    required, additional = skills.split("|")
    required = list(set(required.split(",")))
    additional = list(set(additional.split(",")))
    # print(skill_matcher.perform_search(required, additional, 10))

    response = {"salaries": [20, 20, 20, 20]}
    return json.dumps(response)

@app.route('/salary_map')
def kepler_gl():
    return render_template(KEPLER_FILE)

@app.route('/match_course', methods=['GET'])
def match_course():
    skills = request.args['skills'].lower()
    return courses_finder.perform_search(skills)


# @app.route('/reverse_search', methods=['GET'])
# def reverse_search():
#     skills = request.args['skills'].lower()
#     required, additional = skills.split("|")
#     required = list(set(required.split(",")))
#     additional = list(set(additional.split(",")))
#     print(required, additional)
#     limit = None
#     try:
#         limit = request.args['limit']
#         limit = int(limit)
#     except:
#         limit = None
#     return r_search.perform_search(required, additional, 10)


@app.route('/skill_search', methods=['GET'])
def skill_search():
    skills = request.args['skills'].lower()
    print(skills)
    limit = 5
    try:
        limit = request.args['limit']
        limit = int(limit)
    except:
        pass
    return skill_matcher.perform_search(skills, limit)


@app.route('/search', methods=['GET'])
def search():
    print(request.args['text'])
    return aggregator.search_in_db(request.args['text'],
                                   int(request.args['limit']))


@app.route('/stats', methods=['GET'])
def stats():
    return aggregator.find_coocurring(request.args['skill'])
    # return '''[{"name": "java", "result": 2.2234},
    #         {"name": "c++", "result": 1.24},
    #         {"name": "c", "result": 1.15}]

    #         '''


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
