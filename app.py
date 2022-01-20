from flask import Flask, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
import requests
# from sqlalchemy import desc
# from sqlalchemy.exc import IntegrityError
# import os
# from werkzeug.utils import secure_filename

# from forms import PropAndHeadpieceForm, ProductionForm, RoleForm
from models import db, connect_db
# from user_models import User


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
    return render_template('home.html')

    

@app.route('/get-daily-card')
def get_card():
        
    resp = requests.get(f"{API_BASE_URL}/random?n=1")
    data = resp.json()
    card = data['cards']
    image_url = f"static/cards/{card[0]['name_short']}.jpg"
    return render_template('daily-card.html', card=card, image_url=image_url)

