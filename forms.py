from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms import PasswordField
from wtforms import TextAreaField
from wtforms import HiddenField
from wtforms.validators import InputRequired

class RegisterForm(FlaskForm):
    email = StringField("Email", validators=[InputRequired()])
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    subscribe = None
    
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class ArticleForm(FlaskForm):
    title = StringField("Title", validators=[InputRequired()])
    content = TextAreaField("Content")
    html_render = HiddenField()

class ChangePassword(FlaskForm):
    old_password = PasswordField("Old password", validators=[InputRequired()])
    new_password = PasswordField("New password", validators=[InputRequired()])
