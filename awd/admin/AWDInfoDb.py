from flask_login import UserMixin
import sys
sys.path.append('../../')
from app import db

class AWDInfo(UserMixin, db.Model):
    __tablename__ = 'awdinfo'  # 对应mysql数据库表
    Id = db.Column(db.Integer, primary_key=True)
    teamnum = db.Column(db.String(64), unique=True, index=True)
    dockernum = db.Column(db.String(64), unique=True, index=True)
    dockerimages_webdirs = db.Column(db.String(64), unique=True, index=True)
    # webdirs = db.Column(db.String(64), unique=True, index=True)
    time = db.Column(db.String(64), unique=True, index=True)

    def __init__(self, teamnum,dockernum,dockerimages_webdirs,time):
        self.teamnum = teamnum
        self.dockernum = dockernum
        self.dockerimages_webdirs = dockerimages_webdirs
        # self.webdirs = webdirs
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