from flask import Flask,redirect,url_for,render_template
from flask_moment import Moment
from config import *
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_bootstrap import Bootstrap

app = Flask(__name__)
app.config['SECRET_KEY']='xjusec_hard_to_sauafauuwghaguagv_break'
app.config['SQLALCHEMY_DATABASE_URI'] ='{}://{}:{}@{}:{}/{}'.format(database_type,database_user,database_passwd,database_url,database_port,database_name)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True

bootstrap = Bootstrap(app)
db = SQLAlchemy()
db.init_app(app)
with app.app_context():
    db.create_all()
moment=Moment(app)

login_manger=LoginManager()
login_manger.session_protection='strong'
login_manger.login_view='my_web.login'
login_manger.init_app(app)
@login_manger.user_loader
def load_user(user_id):
    from application.UserDb import Users
    return Users.query.get(int(user_id))

from application.Views import XJUSEC
app.register_blueprint(blueprint=XJUSEC,url_prefix='/XJUSEC')
# print(app.url_map)

@app.errorhandler(404)
def miss(e):
    return render_template('404.html')
@app.errorhandler(500)
def error(e):
    return render_template('500.html')

@app.route('/')
def index():
    return redirect(url_for('my_web.index'))

if __name__ == '__main__':
    app.run()