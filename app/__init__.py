from turtle import title
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
#==============================================================================
from app.config import ProdConfig, DevConfig, TestConfig
#==============================================================================

app = Flask(__name__)


# Assumed Flask environment variable `FLASK_ENV` is added into your path.
if app.config['ENV'] == 'prod':
    app.config.from_object(ProdConfig)
if app.config["ENV"] == 'dev':
    app.config.from_object(DevConfig)
if app.config["ENV"] == 'test':
    app.config.from_object(TestConfig)


db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'



from app import routes
