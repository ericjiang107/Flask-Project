from flask_sqlalchemy import SQLAlchemy
import uuid
import secrets 
from datetime import datetime 
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager
from flask_login import UserMixin
from flask_marshmallow import Marshmallow

login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

db = SQLAlchemy()

ma = Marshmallow()

class User(db.Model, UserMixin):
    id = db.Column(db.String(), primary_key=True, unique=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String, nullable = False)
    token = db.Column(db.String, unique = True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    hero = db.relationship('Hero', backref = 'owner', lazy = True)

# - id (uuid)
# - name (String)
# - email(String)
# - password (String)[Hashed]
# - token (String)[secret]
# - date_created (DateTime)[w/ datetime.utcnow]
# - character (relationship)


    def __init__(self, email, password, token='', id=''):
        self.id = self.set_id()
        self.email = email
        self.password = self.set_password(password)
        self.token = self.get_token(24)

    def set_id(self):
        return str(uuid.uuid4())

    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def get_token(self, length):
        return secrets.token_hex(length)

class Hero(db.Model):
    id = db.Column(db.String, primary_key=True)
    name = db.Column(db.String(150))
    description = db.Column(db.String(200), nullable = True)
    superpower = db.Column(db.String(200))
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable = False) # this references user table (the token). Which person created this
    # data, add that token to the hero table so we know who this belongs to


    def __init__(self, name, description, superpower, user_token, id=''):
        self.id = self.set_id()
        self.name = name
        self.description = description
        self.superpower = superpower
        self.user_token = user_token

    
    def set_id(self):
        return (secrets.token_urlsafe())

    
class HeroSchema(ma.Schema):
    class Meta:
        fields = ['id', 'name', 'description', 'superpower']

hero_schema = HeroSchema()
heroes_schema = HeroSchema(many=True)
