from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_utils import EmailType

db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

class User(db.Model):
    """user info"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.TEXT, nullable=False)
    last_name = db.Column(db.TEXT, nullable=False)
    email = db.Column(db.TEXT, nullable=False)
    phone_number = db.Column(db.TEXT, nullable=True)

    def __repr__(self):
        return f"<User {self.first_name} {self.last_name}, {self.email}>"

class Itinerary(db.Model):

    __tablename__ = "itineraries"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    start_date = db.Column(db.Date)
    end_date = db.Column(db.Date)

    def __repr__(self):
        return f"<start date is {self.start_date}, end date is {self.end_date}>"

class Itinerary_hotel(db.Model):

    __tablename__ = "itinerary_hotels"

    itinerary_id = db.Column(db.Integer, db.ForeignKey("itineraries.id"), nullable=False, primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey("hotels.id"), nullable=False, primary_key=True)

    def __repr__(self):
        return f"<Itinerary Hotel {self.itinerary_id} Song {self.hotel_id}>"

class Itinerary_restaurant(db.Model):

    __tablename__ = "itinerary_restaurants"

    itinerary_id = db.Column(db.Integer, db.ForeignKey("itineraries.id"), nullable=False, primary_key=True)
    rest_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"), nullable=False, primary_key=True)

    def __repr__(self):
        return f"<Itinerary Restaurants {self.itinerary_id} Song {self.rest_id}>"

class Hotel(db.Model):
    
    __tablename__ = "hotels"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    api = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Hotel api {self.api}>"

class Restaurant(db.Model):
    
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    api = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Restaurant api {self.api}>"

class Fav_Hotel(db.Model):

    __tablename__ = "fav_hotels"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, primary_key=True)
    hotel_id = db.Column(db.Integer, db.ForeignKey("hotels.id"), nullable=False, primary_key=True)

    def __repr__(self):
        return f"<Fav Hotel {self.user_id}, {self.hotel_id}>"

class Fav_Rest(db.Model):

    __tablename__ = "fav_restaurants"

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, primary_key=True)
    rest_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"), nullable=False, primary_key=True)

    def __repr__(self):
        return f"<Fav Hotel {self.user_id}, {self.rest_id}>"