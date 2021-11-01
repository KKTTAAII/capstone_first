from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Email, Length
# from wtforms_alchemy import model_form_factory
from models import db, User

# BaseModelForm = model_form_factory(FlaskForm)

# class ModelForm(BaseModelForm):
#     @classmethod
#     def get_session(self):
#         return db.session

class SignupForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(message="Username can't be blank")])
    email = StringField('E-mail', validators=[InputRequired(message="Email can't be blank"), Email()])
    password = PasswordField('Password', validators=[Length(min=6)])