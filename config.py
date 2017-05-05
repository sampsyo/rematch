import os
basedir = os.path.abspath(os.path.dirname(__file__))

SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
SQLALCHEMY_TRACK_MODIFICATIONS = False

WTF_CSRF_ENABLED = True
SECRET_KEY = 'Pr0f3ss0r-ArmS-Is-Br1T1sH'

BASE_URL = 'http://localhost:5000'
PAGINATION_PER_PAGE = 2


# TODO: For Searches through the DB, for example if you wanted to search for a specific professor. 
# Not implemented but put here for ease of use in the future:
# WHOOSH_BASE = os.path.join(basedir, 'search.db')
# MAX_SEARCH_RESULTS = 10
