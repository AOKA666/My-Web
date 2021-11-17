from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from . import db, login_manager
from app import db


class User(db.Model):
    id = 
