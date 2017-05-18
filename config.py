import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

WTF_CSRF_ENABLED = True
SECRET_KEY = 'Pr0f3ss0r-ArmS-Is-Br1T1sH'

BASE_URL = 'http://localhost:5000'
PAGINATION_PER_PAGE = 2

TAGS = [
    'artificial intelligence',
    'computer architecture',
    'computational biology',
    'databases',
    'education',
    'graphics',
    'human computer interaction',
    'operating systems',
    'networking',
    'programming languages',
    'scientific computing',
    'security',
    'theory',
    'natural language processing',
    'algorithms',
    'distributed systems',
    'robotics',
    'information processing',
    'computer vision',
    'ethics',
    'design',
    'compilers',
    'machine learning',
    'other',
    'java',
    'c',
    'c#',
    'c++',
    'python',
    'ocaml',
    'javascript',
    'mongodb',
    'sql'
]

COURSES = [
    'CS 2110',
    'CS 3110',
    'CS 4410',
    'CS 4411',
    'CS 4670',
    'CS 4700',
    'CS 4710',
    'CS 4780',
    'CS 5150',
    'CS 5152',
    'CS 5414',
    'INFO 3450',
    'INFO 4300'
]

# TODO: For Searches through the DB, for example if you wanted to search for a specific professor. 
# Not implemented but put here for ease of use in the future:
# WHOOSH_BASE = os.path.join(basedir, 'search.db')
# MAX_SEARCH_RESULTS = 10
