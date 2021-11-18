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

        mock_user = User(
            email="test@test.com",
            username="testuser",
            password="PASSWORD"
        )
        
        db.session.add(mock_user)
        db.session.commit()

        self.mock_user = mock_user
    
        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        User.query.delete()
        db.session.rollback()
        return res

    #######Test create user#######

    def test_create_user(self):
        """Test that user data is in database"""
        self.assertEqual(self.mock_user.username, "testuser")
        self.assertEqual(self.mock_user.email, "test@test.com")
        self.assertEqual(self.mock_user.password, "PASSWORD")
        self.assertNotEqual(self.mock_user.password, "HASHED_PASSWORD")

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