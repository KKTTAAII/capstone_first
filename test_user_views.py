import os
from unittest import TestCase
from forms import LoginForm
from models import db, User
import json

os.environ['DATABASE_URL'] = "postgresql:///itinerary_test"

from app import app, CURR_USER_KEY

db.drop_all()
db.create_all()

app.config['WTF_CSRF_ENABLED'] = False

class UserViewTestCase(TestCase):
    """Create test client, add sample data."""

    def setUp(self):

        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser")

        db.session.add(self.testuser)
        db.session.commit()

    def tearDown(self):
        res = super().tearDown()
        User.query.delete()
        db.session.rollback()
        return res

    def test_log_in(self):
        """Test if the logged-in user sees the log in page"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id
            resp = c.get("/login", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertIn("Log out", html)

    def test_log_out(self):
        """Test if the logged-out user sees the log in page"""
        with self.client as c:
            resp = c.get("/login", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertIn("Log in", html)
        
    def test_show_user(self):
        """Test if the username shows on the page"""
        with self.client as c:
            with c.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser.id

            resp = c.get(f"/user/{self.testuser.id}")
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn(self.testuser.username, html)

    def test_fail_show_user_when_logged_out(self):
        with self.client as c:
            resp = c.get(f"/user/1", follow_redirects=True)
            html = resp.get_data(as_text=True)
            self.assertEqual(resp.status_code, 200)
            self.assertIn("Access unauthorized.", html)

    
          

   
        
    



    

    