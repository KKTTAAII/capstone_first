import os

from flask import Flask, redirect, render_template, flash, session, g
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Itinerary, Itinerary_hotel, Itinerary_restaurant, Hotel, Restaurant, Fav_Hotel, Fav_Rest
from forms import SignupForm
from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
CURR_USER_KEY = "curr_user"

app.config['SQLALCHEMY_DATABASE_URI'] = (
    os.environ.get('DATABASE_URL', 'postgresql:///user_itinerary'))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "Ktai's project")
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route("/")
def home_page():
     return render_template("home.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    form = SignupForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
            )
            db.session.commit()
        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)
        do_login(user)
        return redirect(f"/user/{user.id}")

    return render_template("signup.html", form=form)


@app.route("/user/<int:user_id>")
def show_user_page(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user_info.html", user=user)

@app.route("/user/<int:user_id>/newiti")
def show_map(user_id):
    return