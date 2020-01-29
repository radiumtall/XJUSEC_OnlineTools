from wtforms import StringField,SubmitField,PasswordField,SelectField
from wtforms.validators import  Required,DataRequired
from flask_wtf import FlaskForm

#登录表单
class Login_Form(FlaskForm):
    name=StringField('name',validators=[Required()])
    pwd=PasswordField('pwd',validators=[Required()])
    submit=SubmitField('Login in')
class Action_Arg(FlaskForm):
    action = SelectField(validators=[DataRequired('默认')],choices=[('all','all'),('time','time'),('url', 'url'), ('ip', 'ip'),('cookie','cookie')],default = 'all',
        coerce=str)
    arg = StringField('arg',validators=[Required()])
    submit = SubmitField('查询')

class HttpMethod(FlaskForm):
    method = SelectField(validators=[DataRequired('默认')],choices=[('get','get'),('post', 'post')],default = 'get',coerce=str)
    url = StringField('url',validators=[Required()])
    posts = StringField('post')
    cookies = StringField('cookie')
    submit = SubmitField('Go!')

class NamePayload(FlaskForm):
    name = StringField('name')
    submit = SubmitField('Go!')