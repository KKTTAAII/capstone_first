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

        mock_user = User(
            email="test@test.com",
            username="testuser",
            password="PASSWORD"
        )
        
        db.session.add(mock_user)
        db.session.commit()

        self.mock_user = mock_user

        mock_iti = Itinerary(
            user_id = mock_user.id,
            iti_name = "Breck2021",
            start_date = "2021-11-18",
            end_date = "2021-11-21"
        )

        db.session.add(mock_iti)
        db.session.commit()

        self.mock_iti = mock_iti

        mock_hotel = Hotel(
            name = "Gravity Haus",
            address = "202 st",
            website = "gh@gmail",
            number = "970-256-8794"
        )
        
        db.session.add(mock_hotel)
        db.session.commit()

        self.mock_hotel = mock_hotel

        mock_rest = Restaurant(
            name = "Cabin Juice",
            address = "200 st",
            website = "cj@gmail",
            number = "970-256-1587"
        )

        db.session.add(mock_rest)
        db.session.commit()

        self.mock_rest = mock_rest

        mock_iti_hotel = Itinerary_hotel(
            itinerary_id = mock_iti.id,
            hotel_id = mock_hotel.id
        )

        db.session.add(mock_iti_hotel)
        db.session.commit()

        self.mock_iti_hotel1 = mock_iti_hotel

        mock_iti_rest = Itinerary_restaurant(
            itinerary_id = mock_iti.id,
            rest_id = mock_rest.id
        )

        db.session.add(mock_iti_rest)
        db.session.commit()

        self.mock_iti_rest = mock_iti_rest

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
                sess[CURR_USER_KEY] = self.mock_user.id 
            resp = c.get(f"/user/{self.mock_user.id}/newiti")
            html = resp.get_data(as_text=True)
            self.assertIn("search", html)
            self.assertIn("Vacation Plan", html)

    def test_not_show_search_when_logged_out(self):
        """Test search form not show when the user is logged out"""
        with self.client as c:
            resp = c.get(f"/user/{self.mock_user.id}/newiti", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertIn("Access unauthorized.", html)
            
    def test_create_itinerary_plan(self):
        """Test create Itinerary"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.mock_user.id 

            info = {
                "hotel": ['The Stanley Hotel,ChIJNeya8fNlaYcRiIZjupMfjgY'],
                "restaurant": ['Cascades Restaurant,ChIJL3e6rfNlaYcR_j8PonDqxlk'],
                "iti_name": "Estes Park 2021",
                "start_date": "2021-11-16",
                "end_date": "2021-11-18"
            }

            resp = c.post(f"/user/{self.mock_user.id}/newiti", data=info, follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertIn(f"{self.mock_user.username}'s Trip!", html)

    def test_delete_itinerary(self):
        """Test delete itinerary"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.mock_user.id 

            mock_iti = Itinerary(
            user_id = self.mock_user.id,
            iti_name = "vail",
            start_date = "2021-11-20",
            end_date = "2021-11-21"
            )

            db.session.add(mock_iti)
            db.session.commit()
            resp = c.post(f"/iti/{mock_iti.id}/delete", follow_redirects=True)
            self.assertEqual(Itinerary.query.get(mock_iti.id), None)
            self.assertEqual(len(Itinerary.query.all()), 1)
        
    def test_show_iti_info(self):
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.mock_user.id 
            
            resp = c.get(f"/iti/1")
            html = resp.get_data(as_text=True)
            self.assertIn("Gravity Haus", html)
            self.assertIn("Cabin Juice", html)