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

    def test_create_itinerary(self):
        """Test that itinerary data is in database"""
        self.assertEqual(self.iti1.iti_name, "Breck2021")
        self.assertEqual(self.iti1.start_date, datetime.date(2021,11,18))
        self.assertEqual(self.iti1.end_date, datetime.date(2021,11,21))
        self.assertEqual(self.iti1.iti_hotels[0].hotels.name, "Gravity Haus")
        self.assertEqual(self.iti1.iti_hotels[0].hotels.address, "202 st")
        self.assertEqual(self.iti1.iti_hotels[0].hotels.website, "gh@gmail")
        self.assertEqual(self.iti1.iti_hotels[0].hotels.number, "970-256-8794")
        self.assertEqual(self.iti1.iti_rests[0].rests.name, "Cabin Juice")
        self.assertEqual(self.iti1.iti_rests[0].rests.address, "200 st")
        self.assertEqual(self.iti1.iti_rests[0].rests.website, "cj@gmail")
        self.assertEqual(self.iti1.iti_rests[0].rests.number, "970-256-1587")

    
        