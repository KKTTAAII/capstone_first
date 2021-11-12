import os
from unittest import TestCase
from models import db, User, Hotel, Restaurant, Itinerary_restaurant, Itinerary_hotel, Itinerary

os.environ['DATABASE_URL'] = "postgresql:///itinerary_test"

from app import app, CURR_USER_KEY

db.drop_all()
db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class ItineraryViewTestCase(TestCase):
    """Create test client, add sample data."""

    def setUp(self):

        db.drop_all()
        db.create_all()

        u1 = User(
            email="test@test.com",
            username="testuser",
            password="PASSWORD"
        )
        
        db.session.add(u1)
        db.session.commit()

        self.u1 = u1

        iti1 = Itinerary(
            user_id = u1.id,
            iti_name = "Breck2021",
            start_date = "2021-11-18",
            end_date = "2021-11-21"
        )

        db.session.add(iti1)
        db.session.commit()

        self.iti1 = iti1

        hotel1 = Hotel(
            name = "Gravity Haus",
            address = "202 st",
            website = "gh@gmail",
            number = "970-256-8794"
        )
        
        db.session.add(hotel1)
        db.session.commit()

        self.hotel1 = hotel1

        rest1 = Restaurant(
            name = "Cabin Juice",
            address = "200 st",
            website = "cj@gmail",
            number = "970-256-1587"
        )

        db.session.add(rest1)
        db.session.commit()

        self.rest1 = rest1

        iti_hotel1 = Itinerary_hotel(
            itinerary_id = iti1.id,
            hotel_id = hotel1.id
        )

        db.session.add(iti_hotel1)
        db.session.commit()

        self.iti_hotel1 = iti_hotel1

        iti_rest1 = Itinerary_restaurant(
            itinerary_id = iti1.id,
            rest_id = rest1.id
        )

        db.session.add(iti_rest1)
        db.session.commit()

        self.iti_rest1 = rest1

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        User.query.delete()
        db.session.rollback()
        return res

    def test_show_search_form_when_logged_in(self):
        """Test if search form shows on the page"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id 
            resp = c.get(f"/user/{self.u1.id}/newiti")
            html = resp.get_data(as_text=True)
            self.assertIn("search", html)
            self.assertIn("Vacation Plan", html)

    def test_not_show_search_when_logged_out(self):
        """Test search form not show when the user is logged out"""
        with self.client as c:
            resp = c.get(f"/user/{self.u1.id}/newiti", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertIn("Access unauthorized.", html)

    def test_create_itinerary_plan(self):
        """Test create Itinerary"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.u1.id 

            data = {
                "hotel": [["The Stanley Hotel,ChIJNeya8fNlaYcRiIZjupMfjgY"]],
                "restaurant": [["Cascades Restaurant,ChIJL3e6rfNlaYcR_j8PonDqxlk"]],
                "iti_name": "Estes Park 2021",
                "start_date": "2021-11-16",
                "end_date": "2021-11-18"
            }
            resp = c.post(f"/user/{self.u1.id}/newiti", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertIn(f"{self.u1.username}'s Trip!", html)