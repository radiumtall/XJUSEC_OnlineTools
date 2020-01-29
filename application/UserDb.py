from flask_login import UserMixin
import sys
sys.path.append('../')
from app import db

class Users(UserMixin, db.Model):
    __tablename__ = 'user'  # 对应mysql数据库表
    Id = db.Column(db.Integer, primary_key=True)
    username_xjusec = db.Column(db.String(64), unique=True, index=True)
    passwd_xjusec = db.Column(db.String(64), unique=True, index=True)

    def __init__(self, name, pwd):
        self.username_xjusec = name
        self.passwd_xjusec = pwd

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