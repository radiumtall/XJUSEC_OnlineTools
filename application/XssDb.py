from flask_login import UserMixin
import sys
sys.path.append('../')
from app import db,login_manger

class Xss(UserMixin, db.Model):
    __tablename__ = 'xss'
    Id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(64), unique=True, index=True)
    ip = db.Column(db.String(64), unique=True, index=True)
    time = db.Column(db.String(64), unique=True, index=True)
    cookie = db.Column(db.String(64), unique=True, index=True)
    def __init__(self, url, ip,time,cookie):
        self.url = url
        self.ip = ip
        self.cookie = cookie
        self.time = time

    def get_id(self):
        return self.Id

    def __repr__(self):
        return '<User %r>' % self.name

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False