import os
from unittest import TestCase

from models import db, User, Hotel, Restaurant, Itinerary, Itinerary_hotel, Itinerary_restaurant
import datetime

os.environ['DATABASE_URL'] = "postgresql:///itinerary_test"

from app import app

db.drop_all()
db.create_all()


class ItineraryModelTestCase(TestCase):
    """Test user model"""

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

    def test_create_itinerary(self):
        """Test that itinerary data is in database"""
        self.assertEqual(self.mock_iti.iti_name, "Breck2021")
        self.assertEqual(self.mock_iti.start_date, datetime.date(2021,11,18))
        self.assertEqual(self.mock_iti.end_date, datetime.date(2021,11,21))
        self.assertEqual(self.mock_iti.iti_hotels[0].hotels.name, "Gravity Haus")
        self.assertEqual(self.mock_iti.iti_hotels[0].hotels.address, "202 st")
        self.assertEqual(self.mock_iti.iti_hotels[0].hotels.website, "gh@gmail")
        self.assertEqual(self.mock_iti.iti_hotels[0].hotels.number, "970-256-8794")
        self.assertEqual(self.mock_iti.iti_rests[0].rests.name, "Cabin Juice")
        self.assertEqual(self.mock_iti.iti_rests[0].rests.address, "200 st")
        self.assertEqual(self.mock_iti.iti_rests[0].rests.website, "cj@gmail")
        self.assertEqual(self.mock_iti.iti_rests[0].rests.number, "970-256-1587")