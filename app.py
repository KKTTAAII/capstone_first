import os
import json
import time
from flask import Flask, redirect, render_template, flash, session, g, request, jsonify
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Itinerary, Itinerary_hotel, Itinerary_restaurant, Hotel, Restaurant
from forms import SignupForm, LoginForm
from sqlalchemy.exc import IntegrityError
import googlemaps
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
API_KEY = os.getenv("API_KEY")
# Define our Client
gmaps = googlemaps.Client(key=API_KEY)
CURR_USER_KEY = "curr_user"
my_fields = [
    'name',
    'website',
    'formatted_address',
    'formatted_phone_number',
    'rating']

errors = {
    "server_err": "Oops, something's wrong. Please try again.",
    "location_not_found": "Location not found. Please enter correct city and state.",
    "results_not_found": "Results not found. Please try again"
}

# Heroku config
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL').replace("://", "ql://", 1) or "postgresql:///user_itinerary"
# local config
# app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
#     'DATABASE_URL', "postgresql:///user_itinerary")
app.config['API_KEY'] = os.environ.get('API_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = True
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "my_key")
toolbar = DebugToolbarExtension(app)

connect_db(app)
db.create_all()

def save_to_database(details, type, iti_type, iti_id):
    if details:
            for detail in details:
                new_place = type(
                    name=detail[0],
                    address=detail[1],
                    number=detail[2],
                    website=detail[3])
                db.session.add(new_place)
                db.session.commit()
                if type == Hotel:
                    new_iti_place = iti_type(
                    itinerary_id=iti_id, hotel_id=new_place.id)
                    db.session.add(new_iti_place)
                    db.session.commit()
                elif type == Restaurant:
                    new_iti_place = iti_type(
                    itinerary_id=iti_id, rest_id=new_place.id)
                    db.session.add(new_iti_place)
                    db.session.commit()


def get_place_details(fields, places):
    all_places_details = []
    for place in places:
        detail_list = []
        details = gmaps.place(place_id=place.split(",")[1], fields=fields)
        place_id = place.split(",")[0]
        detail_list.append(place_id)
        if details:
            address = details["result"]["formatted_address"]
            detail_list.append(address)
        else:
            return
        if details and "formatted_phone_number" in details["result"].keys():
            number = details["result"]["formatted_phone_number"]
            detail_list.append(number)
        else:
            number = ""
            detail_list.append(number)
        if details and "website" in details["result"].keys():
            site = details["result"]["website"]
            detail_list.append(site)
        else:
            site = ""
            detail_list.append(site)
        all_places_details.append(detail_list)
    return all_places_details


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
        return render_template("home/home-user.html")
    else:
        return render_template("home/home.html")


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
            if(constraint == "users_email_key"):
                flash("Email already registered", 'danger')
            if(constraint == "users_username_key"):
                flash("Username already taken", 'danger')
            db.session.rollback()
            return render_template('user/signup.html', form=form)
        do_login(user)
        return redirect(f"/user/{user.id}")

    return render_template("user/signup.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)
        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/")
        else:
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
    if not g.user or g.user.id != user_id:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    ####### handle itinerary form#######

    if request.method == "POST":
        iti_name = request.form.get("iti-name")
        start_date = request.form.get("start_date")
        end_date = request.form.get("end_date")
        hotels = request.form.getlist("hotel")
        restaurants = request.form.getlist("restaurant")

        new_iti = Itinerary(
            iti_name=iti_name,
            user_id=user_id,
            start_date=start_date,
            end_date=end_date)
        db.session.add(new_iti)
        db.session.commit()
        
        hotel_details = get_place_details(my_fields, hotels)
        save_to_database(hotel_details, Hotel, Itinerary_hotel, new_iti.id)

        rest_details = get_place_details(my_fields, restaurants)
        save_to_database(rest_details, Restaurant, Itinerary_restaurant, new_iti.id)

        return redirect(f"/iti/{new_iti.id}")

    return render_template("itinerary/new_iti.html")


###########Itinerary routes###########


@app.route("/iti/<int:iti_id>")
def show_itinerary(iti_id):
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    itinerary = Itinerary.query.get_or_404(iti_id)

    return render_template("itinerary/iti_info.html",
                           iti=itinerary)


@app.route("/user/<int:user_id>/iti")
def show_all_itineraries(user_id):
    if not g.user or g.user.id != user_id:
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
    check_state_list = []
    city_name = ""
    lat = ""
    lng = ""
    places_results = {}
    response = []
    
    # get lat and lng for city and state name
    location = gmaps.geocode(address=f"{city}{state}")
    if location:
        city = location[0]["address_components"][0]["long_name"]
        city_name = city
        lat = location[0]["geometry"]["location"]["lat"]
        lng = location[0]["geometry"]["location"]["lng"]
        lat = lat
        lng = lng
        for obj in location[0]["address_components"]:
            name = obj["short_name"]
            check_state_list.append(name)
    else:
        return jsonify(
            {"result": errors["server_err"]})

    # check that there is a city in that state
    if city_name.capitalize() == city.capitalize() and state in check_state_list:
        params = {
        'location': (lat,lng),
        'type':type,
        'rank_by':"distance",
    }
        result = gmaps.places_nearby(**params)

        for key in result:
            places_results[key] = result[key]
        # get all results up to 60 max per googlemaps
        while result.get('next_page_token'):
            next_page = result['next_page_token']
            time.sleep(2)
            more_results = gmaps.places_nearby(page_token=next_page, **params)
            result = more_results
            places_results["results"].extend(result["results"])
                
    else:
        return jsonify(
            {"result": errors["location_not_found"]})

    # get place details
    if(places_results["status"] == "OK"):
        for place in places_results['results']:
            my_place_id = place["place_id"]
            place_details = gmaps.place(
                place_id=my_place_id, fields=my_fields)
            place_details["place_id"] = my_place_id
            place_details["location"] = place["geometry"]["location"]
            response.append(place_details)
        return jsonify(response)
    else:
        return jsonify({"result": errors["results_not_found"]})


#################Error page handlers################


@app.errorhandler(404)
def page_not_found(e):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def page_not_found(e):
    return render_template('errors/500.html'), 500