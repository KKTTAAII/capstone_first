import os

from flask import Flask, json, redirect, render_template, flash, session, g, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Itinerary, Itinerary_hotel, Itinerary_restaurant, Hotel, Restaurant, Fav_Hotel, Fav_Rest
from forms import SignupForm, LoginForm, EditUsernameForm
import requests
import googlemaps
import pprint
import time


API_KEY = ""
#Define our Client
gmaps = googlemaps.Client(key = API_KEY)


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


@app.route("/user/<int:user_id>", methods=["GET", "POST"])
def show_user_page(user_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = g.user    
    form = LoginForm(obj=user)
    if form.validate_on_submit():
        if User.authenticate(user.username, form.password.data):
            user.username = form.username.data
            db.session.commit()
            return redirect(f"/user/{user_id}")

    user = User.query.get_or_404(user_id)
    return render_template("user/user_info.html", user=user, form=form)


@app.route("/user/<int:user_id>/newiti", methods=["GET", "POST"])
def add_new_itinerary(user_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    ####### handle itinerary form#######

    if request.method == "POST":
        iti_name = request.form.get("iti-name")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        hotels = request.form.getlist("hotel")
        restaurants = request.form.getlist("restaurant")

        new_iti = Itinerary(iti_name=iti_name,user_id=user_id, start_date=start_date, end_date=end_date)
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
        return redirect(f"/iti/{new_iti.id}")

    return render_template("itinerary/new_iti.html")


###########Itinerary routes########


@app.route("/iti/<int:iti_id>")
def show_itinerary(iti_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    itinerary = Itinerary.query.get_or_404(iti_id)
    return render_template("itinerary/iti_info.html", itinerary=itinerary)


@app.route("/user/<int:user_id>/iti")
def show_all_itineraries(user_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    user = User.query.get_or_404(user_id)
    all_iti = user.itineraries
    return render_template("itinerary/all_iti.html", all_iti=all_iti)


@app.route("/iti/<int:iti_id>/delete", methods=["POST"])
def delete_itinerary(iti_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    itinerary = Itinerary.query.get_or_404(iti_id)
    db.session.delete(itinerary)
    db.session.commit()
    return redirect(f"/user/{g.user.id}/iti")


@app.route("/iti/search")
def find_places():
    city = request.args.get("city")
    type = request.args.get("type")
    state = request.args.get("state")
    result = []
    ##get lat and lng for city and state name
    locations = gmaps.geocode(address=f"{city}{state}")
    if locations:
        for location in locations:
            city_name = location["address_components"][0]["long_name"]
            state_name1 = location["address_components"][2]["short_name"]
            state_name2 = location["address_components"][3]["short_name"]
            lat = location["geometry"]["location"]["lat"]
            lng = location["geometry"]["location"]["lng"]
            if city_name.capitalize() == city.capitalize() and state in [state_name1, state_name2]:
                lat = lat
                lng = lng
            ###make request for all places using lat, long
                places_result = gmaps.places_nearby(location=(lat,lng), type=type, rank_by = "distance")
                if(places_result["status"] == "OK"):
                    for place in places_result['results']:
                        my_place_id = place["place_id"]
                        my_fields = ['name', 'website', 'formatted_address', 'formatted_phone_number', 'rating']
            ###make request for details
                        place_details = gmaps.place(place_id = my_place_id, fields = my_fields)
                        place_details["place_id"] = my_place_id
                        result.append(place_details)
                    return jsonify(result)
                else: 
                    return jsonify({"result": "Results not found. Please try again"})
            else: 
                return jsonify({"result": "Location not found. Please enter correct city and state."})
    else:
        return jsonify({"result":"Oops, something's wrong. Please try again."})
    
