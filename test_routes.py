"""Routes tests."""

# run these tests like:
#
#    FLASK_ENV=production python -m unittest test_routes.py


import os
from unittest import TestCase
import datetime
from flask import g

from models import db, User, Card


os.environ['DATABASE_URL'] = "postgresql:///tarot_test"


from app import app, CURR_USER_KEY

db.create_all()

app.config['WTF_CSRF_ENABLED'] = False


class CardRoutesTestCase(TestCase):
    """Test routes for all routes."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        self.client = app.test_client()

        self.testuser = User.signup(username="testuser",
                                    email="test@test.com",
                                    password="testuser")
        self.testuser_id = 8989
        self.testuser.id = self.testuser_id

        db.session.commit()

        today = datetime.date.today()
        yesterday = today - datetime.timedelta(days = 1)
        old_date = today - datetime.timedelta(days=4)

        c1 = Card(
            card_name="te67",
            card_name_long="test card",
            notes="testing notes", 
            timestamp=yesterday,
            user_id=self.testuser.id
        )

        c2 = Card(
            id=9999,
            card_name="ar10",
            card_name_long="Wheel Of Fortune",
            notes="actual card for testing connection to API", 
            timestamp=old_date,
            user_id=self.testuser.id
        )

        self.c1 = c1
        self.c2 = c2

        db.session.add(c1)
        db.session.add(c2)
        db.session.commit()

        with self.client.session_transaction() as sess:
                sess[CURR_USER_KEY] = self.testuser_id
                g.user = User.query.get(sess[CURR_USER_KEY])

    
    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res



    def test_login(self):
        with self.client as c:
            resp = c.get("/login")
            self.assertEqual(resp.status_code, 200)

            resp2 = c.post("/login", data={"username": "testuser", "password": "testuser"})
            # Make sure it redirects
            self.assertEqual(resp2.status_code, 302)

    
    def test_dashboard(self):
        with self.client as c:
            resp = c.get("/dashboard")

            self.assertEqual(resp.status_code, 200)
            self.assertIn("testuser", str(resp.data))
            self.assertIn("Wheel Of Fortune", str(resp.data))


    def test_card_detail(self):
        with self.client as c:
            resp = c.get("/cards/9999")

            self.assertIn("Wheel Of Fortune", str(resp.data))
            self.assertEqual(resp.status_code, 200)


    def test_daily_card(self):
        with self.client as c:
            resp = c.get("/get-daily-card")

            self.assertEqual(resp.status_code, 200)
            

    def test_card_notes(self):
        with self.client as c:
            resp = c.get("/notes/9999")

            self.assertIn("Update Notes", str(resp.data))
            self.assertEqual(resp.status_code, 200)

            resp2 = c.post("/notes/9999", data={"notes": "updating notes for test"})
            # Make sure it redirects
            self.assertEqual(resp2.status_code, 302)


    