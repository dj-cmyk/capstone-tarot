# Daily Tarot Card App

### Link to Deployed App

https://tarot-daily-app.herokuapp.com/login

### General Details about the app

Daily Tarot Card App allows users to generate one rondom card from the standard tarot deck each day, see the upright and reversed meanings of the card, as well as an image and description of the card visuals, and to keep their own personal notes about that specific card on that day. 

Each user is only allowed to generate one card to their account each day, in order for them to focus on the meanings of that card. I was hoping that people would use this as a way to familiarize themselves with the cards if they were new to reading tarot, or as a way to keep records of personal meanings to each card.  

### Standard User Flow

Users are able to sign up for an account on the sign up page, where they must enter a valid email address, username, and password. They will then be redirected to the user dashboard page where they can see any cards previously generated, as well as a button to generate a card for today, and a menu with links to logout or return to their dashboard. 

Once the user presses the button to get their daily card, they will be redirected to a page containing an image of the card they selected, as well as information about the card description and meanings, and an option to add notes for that particular card on that particular day. Whether or not they add notes to the card, that card will be added to their user dashboard where they will be able to see the notes and date the card was generated. 

If a user has already selected a card for that particular day, the app will inform them when they try to generate a new card that they have already done so, and will ask them to come back tomorrow. 

### Link to external API for tarot card meanings

https://github.com/ekelen/tarot-api


### Technology used to build this app

Python, Flask, SQLAlchemy, HTML, bootstrap, deplpoyed on heroku




