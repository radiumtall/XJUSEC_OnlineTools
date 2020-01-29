from wtforms import StringField,SubmitField,PasswordField,SelectField
from wtforms.validators import  Required,DataRequired
from flask_wtf import FlaskForm

class Control__off(FlaskForm):
    teamnum = StringField('teamnum',validators=[Required()])
    dockernum = SelectField(validators=[DataRequired('默认')],choices=[('1','1'),('2', '2'),('3','3'),('4','4'),('5','5'),('6','6')],default = '1',coerce=str)
    dockerimages_webdirs = StringField('dockerimages:webdirs', validators=[Required()])
    # webdirs = StringField('webdirs',validators=[Required()])
    time = SelectField(validators=[DataRequired('默认')],choices=[('2h','2h'),('3h', '3h'),('4h','4h'),('5h','5h'),('6h','6h'),('7h','7h')],default = '2h',coerce=str)
    submit = SubmitField('Go!')