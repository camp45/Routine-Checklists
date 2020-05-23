from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.config.from_object(Config)
app.debug = True
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = 'login'

toolbar = DebugToolbarExtension(app)

from cl_app import routes, models, errors

