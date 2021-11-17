from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import config
from flask_migrate import Migrate


app = Flask(__name__)
app.config.from_object(Config)
bootstrap = Bootstrap(app)
##db = SQLAlchemy(app)
##login_manager = LoginManager(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

##def create_app(config_name):
##    app = Flask(__name__)
##    app.config.from_object(config[config_name])
##    config[config_name].init_app(app)
##
##    bootstrap.init_app(app)
##    db.init_app(app)
##    login_manager.init_app(app)
##    return app

from app import views, models
