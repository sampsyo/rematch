from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
from apscheduler.schedulers.background import BackgroundScheduler
import utils

# NOTE: Need to do this once we enable searching with the db using whoosh
# from config import basedir


app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['ALLOWED_EXTENSIONS'] = set(
    ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'doc', 'docx'])
app.config['MAX_CONTENT_LENGTH'] = 1000000

if not os.path.isdir('uploads/'):
    os.mkdir('uploads/')

from server.views import *
from routes import *
from models import Professor, Student

scheduler = BackgroundScheduler()
scheduler.start()
scheduler.add_job(utils.disable_stale_posts, 'interval', days=1)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(userid):
    return (Professor.query.filter(Professor.net_id == userid).first() or
            Student.query.filter(Student.net_id == userid).first())
