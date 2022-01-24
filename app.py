from flask import Flask, render_template, request, flash, redirect, session, g
from flask_debugtoolbar import DebugToolbarExtension
import requests
# from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from datetime import date
# import os
# from werkzeug.utils import secure_filename

from forms import NotesForm, UserAddForm, LoginForm
from models import db, connect_db, User, Note, Card


CURR_USER_KEY = "curr_user"
today = date.today()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///tarot_app_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'secretANDrandom101010'

# app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024  # 8MB max-limit.

# debug = DebugToolbarExtension(app)

connect_db(app)

API_BASE_URL = "https://rws-cards-api.herokuapp.com/api/v1/cards"

# ***********************************************************************************
# Routes
# ***********************************************************************************

@app.route('/')
def display_homepage():
    '''docstring'''
    return render_template('home.html', today=today)

    

@app.route('/get-daily-card', methods=["GET", "POST"])
def get_card():
    
    # if user not logged in, this shouldn't work and redirect to login page

    # if a card has already been selected + saved for today, this should redirect to user home page with daily/weekly/monthly overview


    resp = requests.get(f"{API_BASE_URL}/random?n=1")
    data = resp.json()
    card = data['cards']
    image_url = f"static/cards/{card[0]['name_short']}.jpg"

    form = NotesForm()

    if form.validate_on_submit():
        note = Note(
            text=form.notes.data,
            user_id=g.user.id
        )
        card = Card(
            card_name = card[0]['name_short'],
            user_id = g.user.id
        )

        db.session.add(note)
        db.session.add(card)
        db.session.commit()

        return redirect("/")

    else:
        return render_template('daily-card.html', card=card, image_url=image_url, today=today, form=form)



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
                image_url=form.image_url.data or User.image_url.default.arg,
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('signup.html', form=form)

        do_login(user)

        return redirect("/")

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
            return redirect("/")

        flash("Invalid credentials.", 'danger')

    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]
        flash(f"You have successfully logged out!", "success")
    return redirect('/login')