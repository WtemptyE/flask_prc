from flask import Flask, g
from config import Configuration

from flask_sqlalchemy import SQLAlchemy  # Support SQLAlchemy

from flask_migrate import Migrate, MigrateCommand  # Support flask-migrate to generate database
from flask_script import Manager  # Support Manager to app

from flask_login import LoginManager, current_user  # user support

from flask_bcrypt import Bcrypt

app = Flask(__name__)

app.config.from_object(Configuration)
db = SQLAlchemy(app)  # Connect database file to this application

Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

login_manager = LoginManager(app)
login_manager.login_view = "login"

@app.before_request
def _before_request():
    g.user = current_user

from flask import request, session  # Cheak about last page visit use session

@app.before_request
def _last_page_visited():
    if "current_page" in session:
        session["last_page"] = session["current_page"]
    session["current_page"] = request.path

bcrypt = Bcrypt(app)

from flask_restless import APIManager
api = APIManager(app, flask_sqlalchemy_db=db)