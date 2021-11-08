from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Email, Length, ValidationError
from wtforms.fields.html5 import DateField
from models import Restaurant, db, User


class SignupForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(message="Username can't be blank")])
    email = StringField("E-mail", validators=[InputRequired(message="Email can't be blank"), Email()])
    password = PasswordField("Password", validators=[Length(min=6)])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(message="Username can't be blank")])
    password = PasswordField("Password", validators=[Length(min=6)])


