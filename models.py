from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import uuid
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask_login import LoginManager
from flask_marshmallow import Marshmallow
import secrets

login_manager = LoginManager()
ma = Marshmallow()
db = SQLAlchemy()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

class User(db.Model, UserMixin):
    id = db.Column(db.String, primary_key=True)
    email = db.Column(db.String(150), nullable=False)
    password = db.Column(db.String, nullable=False, default='')
    g_auth_verify = db.Column(db.Boolean, default=False)
    token = db.Column(db.String, default='', unique=True)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __init__ (self, email, password, token='', g_auth_verify=False):
        self.id = self.set_id()
        self.password = self.set_password(password)
        self.email = email
        self.token = self.set_token(24)
        self.g_auth_verify = g_auth_verify

    def set_token(self, length):
        return secrets.token_hex(length)

    def set_id(self):
        return str(uuid.uuid4())
    
    def set_password(self, password):
        self.pw_hash = generate_password_hash(password)
        return self.pw_hash

    def __repr__(self):
        return f'User {self.email} has been added to the database'
    
class Meme(db.Model):
    id = db.Column(db.String, primary_key=True)
    image_source = db.Column(db.String, nullable=False)
    meme_text = db.Column(db.String(200), default='')
    user_token = db.Column(db.String, db.ForeignKey('user.token'), nullable=False)

    def __init__(self, image_source, meme_text, user_token, id=''):
        self.id = self.set_id()
        self.image_source = image_source
        self.meme_text = meme_text
        self.user_token = user_token

    def __repr__(self):
        return f'Meme has been added to your library'
    
    def set_id(self):
        return (secrets.token_urlsafe())

class MemeSchema(ma.Schema):
    class Meta:
        fields = ['id', 'image_source', 'meme_text']

meme_schema = MemeSchema()
memes_schema = MemeSchema(many=True)