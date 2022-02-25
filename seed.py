from app import db
from models import User, Card


db.drop_all()
db.create_all()



user1 = User(username="sampleuser", email="sampleemail@sample.email.com", password="samplepassword1")

db.session.add(user1)
db.session.commit()


card1 = Card(card_name='cuac', card_name_long='Ace of Cups', notes="notes on ace of cups", timestamp='2022-01-28 00:00:00', user_id=1)
card2 = Card(card_name='cu02', card_name_long='Two of Cups', notes="notes on two of cups", timestamp='2022-01-26 00:00:00', user_id=1)
card3 = Card(card_name='cu03', card_name_long='Three of Cups', notes="notes on three of cups", timestamp='2022-01-25 00:00:00', user_id=1)

db.session.add_all([card1, card2, card3])
db.session.commit()
