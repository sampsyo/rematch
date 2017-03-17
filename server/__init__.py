from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# NOTE: Need to do this once we enable searching with the db using whoosh
# from config import basedir


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)


from server.views import *
from routes import *
