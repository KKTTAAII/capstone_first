import os
from unittest import TestCase

from models import db, User

os.environ['DATABASE_URL'] = "postgresql:///itinerary_test"

from app import app

db.drop_all()
db.create_all()

class UserModelTestCase(TestCase):
    """Test user model"""

    def setUp(self):
        db.drop_all()
        db.create_all()

        u1 = User(
            email="test@test.com",
            username="testuser",
            password="PASSWORD"
        )

        u2 = User(
            email="test2@test.com",
            username="testuser2",
            password="PASSWORD2"
        )

        db.session.add_all([u1,u2])
        db.session.commit()

        self.u1 = u1
        self.u2 = u2

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        User.query.delete()
        db.session.rollback()
        return res

    #######Test create user#######

    def test_user_model(self):
        """Test that user data is in database"""
        self.assertEqual(self.u1.username, "testuser")
        self.assertEqual(self.u1.email, "test@test.com")
        self.assertEqual(self.u1.password, "PASSWORD")
        self.assertNotEqual(self.u1.password, "HASHED_PASSWORD")

    def test_create_user_fail(self):
        with self.assertRaises(TypeError) as context:
            User.signup("testuser", "test@test.com")

    #######Test authenticate user#######

    def test_authenticate_user(self):
        test = User.signup("testuser3", "test3@test.com", "PASSWORD3")
        db.session.commit()
        test_auth = User.authenticate("testuser3", "PASSWORD3")
        self.assertEqual(test_auth.id, test.id)
        self.assertTrue(test_auth)

    def test_authenticate_user_wrong_username(self):
        test = User.signup("testuser3", "test3@test.com", "PASSWORD3")
        db.session.commit()
        test_auth = User.authenticate("nkfslgb", "PASSWORD3")
        self.assertFalse(test_auth)

    def test_authenticate_user_wrong_username(self):
        test = User.signup("testuser3", "test3@test.com", "PASSWORD3")
        db.session.commit()
        test_auth = User.authenticate("testuser3", "sjgfohnofdhn")
        self.assertFalse(test_auth)
