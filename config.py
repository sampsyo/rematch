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
        'information theory',
        'computer vision',
        'ethics',
        'design',
        'compilers',
        'machine learning',
        'algorithms',
        'computer performance analysis',
        'cryptography',
        'software engineering',
        'cognitive science',
        'data science',
        'neural networks',
        'deep learning',
        'other',
        'java',
        'c',
        'c#',
        'c++',
        'python',
        'ocaml',
        'javascript',
        'mongodb',
        'sql',
        'r',
        'php',
        'xml',
        'android',
        'swift',
        'objective-c',
        'matlab',
        'ruby',
        'unix',
        'linux',
        'windows',
        'assembly',

    ]

    COURSES = [
        'CS 1110',
        'CS 1112',
        'CS 2800',
        'CS 2110',
        'CS 3110',
        'CS 3300',
        'CS 3410',
        'CS 3420',
        'CS 4110',
        'CS 4120',
        'CS 4320',
        'CS 4410',
        'CS 4411',
        'CS 4420',
        'CS 4620',
        'CS 4670',
        'CS 4700',
        'CS 4701',
        'CS 4740',
        'CS 4744',
        'CS 4780',
        'CS 4786',
        'CS 4820',
        'CS 4830',
        'CS 4860',
        'CS 5150',
        'CS 5152',
        'CS 5413',
        'CS 5414',
        'CS 5430',
        'CS 5431',
        'CS 6110',
        'CS 6320',
        'CS 6410',
        'CS 6700',
        'CS 6784',
        'CS 6820',
        'INFO 2450',
        'INFO 3300',
        'INFO 3450',
        'INFO 4300',
        'INFO 5300'
    ]

# TODO: For Searches through the DB, for example if you wanted to search for a specific professor. 
# Not implemented but put here for ease of use in the future:
# WHOOSH_BASE = os.path.join(basedir, 'search.db')
# MAX_SEARCH_RESULTS = 10
