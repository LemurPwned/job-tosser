import json
import os

from flask import Flask, render_template, request
from flask_cors import CORS

from aggregator import Aggregator
from courses_finder import CoursesFinder
from reverse_search import ReverseSearch
from ast import literal_eval

app = Flask(__name__)

CORS(app)

DATA_LOC = '../data'
INDEX_FILE = 'index.html'
KEPLER_FILE = 'kepler.gl.html'
SKILL_SUBPAGE = "skill.html"


DATABASE = os.path.join(DATA_LOC, 'DATABASE.pkl')
REVERSE_DATABASE = os.path.join(DATA_LOC, 'DATABASE.pkl')
COURSE_DATABASE = os.path.join(DATA_LOC, 'res.csv')

aggregator = Aggregator(DATABASE)
r_search = ReverseSearch(REVERSE_DATABASE)
courses_finder = CoursesFinder(COURSE_DATABASE)


@app.route('/')
def root():
    return render_template(INDEX_FILE)

@app.route('/skill', methods=['GET'])
def skill():
    skill = request.args['skill'].lower()
    course = courses_finder.perform_search(skill)
    name = course['course']
    link = "udacity.com/" + course['link']
    desc = course['desc']
    level = course['level']
    color_dict = {"beginner": "btn btn-success", "intermediate": "btn btn-warning", "advanced": "btn btn-danger"}
    estimated_time = course['estimated_time']
    tags = list(course['skills'])
    #j = json.loads(course)
    

    return render_template(SKILL_SUBPAGE, skill_name = skill, \
        course = name, link=link, description=desc, 
        level_color=color_dict[level], level=level, est_time=estimated_time, \
        tags=tags)

@app.route('/salary_map')
def kepler_gl():
    return render_template(KEPLER_FILE)


@app.route('/match_course', methods=['GET'])
def match_course():
    skills = request.args['skills'].lower()
    return courses_finder.perform_search(skills)


@app.route('/reverse_search', methods=['GET'])
def reverse_search():
    skills = request.args['skills'].lower()
    required, additional = skills.split("|")
    required = list(set(required.split(",")))
    additional = list(set(additional.split(",")))
    print(required, additional)
    limit = None
    try:
        limit = request.args['limit']
        limit = int(limit)
    except:
        limit = None
    return r_search.perform_search(required, additional, 10)


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
    app.run(host="0.0.0.0")
