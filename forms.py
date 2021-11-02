from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField
from wtforms.validators import InputRequired, Email, Length, ValidationError
from wtforms.fields.html5 import DateField
# from wtforms_alchemy import model_form_factory
from models import Restaurant, db, User

# BaseModelForm = model_form_factory(FlaskForm)

# class ModelForm(BaseModelForm):
#     @classmethod
#     def get_session(self):
#         return db.session

class SignupForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(message="Username can't be blank")])
    email = StringField("E-mail", validators=[InputRequired(message="Email can't be blank"), Email()])
    password = PasswordField("Password", validators=[Length(min=6)])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired(message="Username can't be blank")])
    password = PasswordField("Password", validators=[Length(min=6)])

# class ItineraryForm(FlaskForm):
#     start_date = DateField("Start Date", format='%m-%d-%Y')
#     end_date = DateField("End Date", format='%m-%d-%Y')
#     hotel = StringField("Hotel")
#     restaurant = StringField("Restaurant")

def validate_start_date(form, field):
        if not field.data:
            raise ValidationError("Start date must be entered")

def validate_end_date(form, field):
        if not field.data:
            raise ValidationError("End date must be entered")