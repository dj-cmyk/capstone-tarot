from sqlite3 import Timestamp
from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
import requests
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from datetime import date
# import os
# from werkzeug.utils import secure_filename

from forms import NotesForm, UserAddForm, LoginForm
from models import db, connect_db, User, Card


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///tarot_app_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secretANDrandom101010'


# debug = DebugToolbarExtension(app)

connect_db(app)

CURR_USER_KEY = "curr_user"
API_BASE_URL = "https://rws-cards-api.herokuapp.com/api/v1/cards"

# ***********************************************************************************
# Routes
# ***********************************************************************************

@app.route('/')
def display_homepage():
    '''docstring'''
    return redirect('/login')

    

@app.route('/get-daily-card', methods=["GET", "POST"])
def get_card():
    '''docstring'''

    # if user not logged in, this shouldn't work and redirect to login page
    if not g.user:
        return redirect('/login')

    else:
        # if a card has already been selected + saved for today, this should redirect to dashboard
        if Card.query.filter(
            Card.user_id == g.user.id, 
            Card.timestamp == date.today()).all():
            flash("Card for Today already chosen, come back tomorrow", 'warning')
            return redirect('/dashboard')

        else:
            resp = requests.get(f"{API_BASE_URL}/random?n=1")
            data = resp.json()
            card = data['cards']
            ref_card = card[0]['name_short']
            image_url = f"static/cards/{ref_card}.jpg"
            today = date.today()
            # this is not working because it's saving the card to the DB and then not letting me add notes to it due to it already being in the db, but when I try to add it after typing the notes, it is selecting a different random card and adding that to the db instead. I think I need to add to the db when I submit the form with the notes and do all of it together but I don't know how to get it so it doesn't pick another card from the api - how do i save the state of the card basically?
            new_card = Card(
                    card_name = ref_card,
                    card_name_long = card[0]['name'],
                    user_id = g.user.id, 
                )
            db.session.add(new_card)
            db.session.commit()


            form = NotesForm()

            if form.validate_on_submit():
                new_card.notes = form.notes.data
                db.session.commit()
                return redirect("/dashboard")

            else:
                return render_template('daily-card.html', card=card, image_url=image_url, today=today, form=form)


@app.route('/dashboard')
def show_dashboard():
    '''docstring'''
    if not g.user:
        return redirect('/login')
    else:
        user_id = g.user.id
        today = date.today()

        cards = Card.query.filter_by(user_id = user_id).order_by(Card.timestamp.desc())
        

        return render_template('dashboard.html', today=today, cards=cards)

##############################################################################
# User signup/login/logout


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = UserAddForm()

    if form.validate_on_submit():
        try:
            user = User.signup(
                username=form.username.data,
                password=form.password.data,
                email=form.email.data,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/dashboard")

    else:
        return render_template('signup.html', form=form)


@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            flash(f"Hello, {user.username}!", "success")
            return redirect("/dashboard")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
        flash(f"You have successfully logged out!", "success")
    return redirect('/login')