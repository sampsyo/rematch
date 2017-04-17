from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# NOTE: Need to do this once we enable searching with the db using whoosh
# from config import basedir


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

from server.views import *
from routes import *
from models import Professor, Student

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(userid):
    return (Professor.query.filter(Professor.net_id == userid).first() or
            Student.query.filter(Student.net_id == userid).first())
