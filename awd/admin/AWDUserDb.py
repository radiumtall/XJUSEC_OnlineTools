from flask_login import UserMixin
import sys
sys.path.append('../../')
from app import db

class Users(UserMixin, db.Model):
    __tablename__ = 'awduser'  # 对应mysql数据库表
    Id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, index=True)
    pwd = db.Column(db.String(64), unique=True, index=True)
    status = db.Column(db.String(64), unique=True, index=True)
    sshpwd = db.Column(db.String(64), unique=True, index=True)
    def __init__(self, name, pwd,status,sshpwd):
        self.name = name
        self.pwd = pwd
        self.status = status
        self.sshpwd = sshpwd
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