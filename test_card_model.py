"""Card model tests."""

# run these tests like:
#
#    python -m unittest test_card_model.py


import os
from unittest import TestCase

from models import db, User, Card


os.environ['DATABASE_URL'] = "postgresql:///tarot_test"


from app import app


db.create_all()



class CardModelTestCase(TestCase):
    """Test model for users."""

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u1 = User.signup("test1", "email1@email.com",  "password")
        uid1 = 11111
        u1.id = uid1

        db.session.commit()

        u1 = User.query.get(uid1)

        self.u1 = u1
        self.uid1 = u1.id

        self.client = app.test_client()
    
    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res

    def test_card_model(self):
        """Does basic model work?"""

        c = Card(
            card_name="te67",
            card_name_long="test card",
            notes="testing notes", 
            user_id=self.u1.id
        )

        db.session.add(c)
        db.session.commit()

        # user should have one card linked to their userID
        self.assertEqual(len(self.u1.cards), 1)
