from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import time

LAST_CLEANUP = None


# Create the Flask app and its database.
app = Flask(__name__)
app.config.from_object('config')
db = SQLAlchemy(app)

# Import the application components, which register themselves.
from server.models import Professor, Student, Post  # noqa
from server import views  # noqa
from server import routes  # noqa


# Periodically look for stale posts and disable them.
@app.before_request
def cleanup():
    global LAST_CLEANUP
    now = time.time()
    if not LAST_CLEANUP or (now - LAST_CLEANUP >
                            app.config['CLEANUP_INTERVAL']):
        Post.disable_stale_posts()
        LAST_CLEANUP = now


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(userid):
    return (Professor.query.filter(Professor.net_id == userid).first() or
            Student.query.filter(Student.net_id == userid).first())
