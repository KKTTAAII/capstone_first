import os

from flask import Flask, redirect, render_template, flash, session, g, request
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Itinerary, Itinerary_hotel, Itinerary_restaurant, Hotel, Restaurant, Fav_Hotel, Fav_Rest
from forms import SignupForm, LoginForm, validate_end_date, validate_start_date
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

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])
    else:
        g.user = None


def do_login(user):

    session[CURR_USER_KEY] = user.id


def do_logout():

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]

############root route#############


@app.route("/")
def home_page():
    if g.user:
        return render_template("home-user.html")
    else:
        return render_template("home.html")


###########signup, login, logout routes##############


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
        except IntegrityError as e:
            constraint = e.orig.diag.constraint_name
            print(constraint)
            if(constraint == "users_email_key"):
                flash("Email already registered", 'danger')
            if(constraint == "users_username_key"):
                flash("Username already taken", 'danger')
            db.session.rollback()
            return render_template('user/signup.html', form=form)
        do_login(user)
        return redirect(f"/user/{user.id}")

    return render_template("user/signup.html", form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    
    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('user/login.html', form=form)


@app.route("/logout")
def logout():

    session.pop(CURR_USER_KEY)
    flash("You are logged out!", "info")
    return redirect("/")


################User routes##############


@app.route("/user/<int:user_id>")
def show_user_page(user_id):
    user = User.query.get_or_404(user_id)
    return render_template("user/user_info.html", user=user)

@app.route("/user/<int:user_id>/newiti", methods=["GET", "POST"])
def add_new_itinerary(user_id):
    if request.method == "POST":
        # validate_start_date
        # validate_end_date
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        hotels = request.form.getlist("hotel")
        restaurants = request.form.getlist("restaurant")

        new_iti = Itinerary(user_id=user_id, start_date=start_date, end_date=end_date)
        db.session.add(new_iti)
        db.session.commit()

        for hotel in hotels:
            new_hotel = Hotel(name=hotel)
            db.session.add(new_hotel)
            db.session.commit()
            new_hotel_iti = Itinerary_hotel(itinerary_id=new_iti.id, hotel_id=new_hotel.id)
            db.session.add(new_hotel_iti)
            db.session.commit()
        for rest in restaurants:
            new_rest = Restaurant(name=rest)
            db.session.add(new_rest)
            db.session.commit()
            new_rest_iti = Itinerary_restaurant(itinerary_id=new_iti.id, rest_id=new_rest.id)
            db.session.add(new_rest_iti)
            db.session.commit()
        return redirect(f"/user/{user_id}/iti/{new_iti.id}")

    return render_template("itinerary/new_iti.html")


###########Itinerary routes########


@app.route("/user/<int:user_id>/iti/<int:iti_id>")
def show_itinerary(user_id, iti_id):
    itinerary = Itinerary.query.get_or_404(iti_id)
    
    return render_template("itinerary/iti_info.html", itinerary=itinerary)

@app.route("/user/<int:user_id>/itis")
def show_all_itineraries(user_id):
    user = User.query.get_or_404(user_id)
    all_iti = user.itineraries
    return render_template("itinerary/all_iti.html", all_iti=all_iti)