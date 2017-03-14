from flask import Flask
from flask_sqlalchemy import SQLAlchemy
# from config import basedir  NOTE: Need to do this once we enable searching with the db using whoosh

app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from app import views, models, api
