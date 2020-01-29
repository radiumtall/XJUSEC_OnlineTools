import sys
sys.path.append('../')
from app import db
class Blog(db.Model):
    __tablename__ = 'blog'
    Id = db.Column(db.Integer, primary_key=True)
    url = db.Column(db.String(64), unique=True, index=True)
    title = db.Column(db.String(64), unique=True, index=True)
    time = db.Column(db.String(64), unique=True, index=True)
    src = db.Column(db.String(64), unique=True, index=True)
    num = db.Column(db.Integer, unique=True, index=True)
    def __init__(self, url, title,time,src,num):
        self.url = url
        self.title = title
        self.time = time
        self.src = src
        self.num = num

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