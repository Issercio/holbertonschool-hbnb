from flask import Blueprint, render_template

web_routes = Blueprint('web_routes', __name__)

@web_routes.route('/')
def home():
    return render_template('index.html')

@web_routes.route('/login')
def login():
    return render_template('login.html')

@web_routes.route('/place')
def place():
    return render_template('place.html')

@web_routes.route('/add_review')
def add_review():
    return render_template('add_review.html')
