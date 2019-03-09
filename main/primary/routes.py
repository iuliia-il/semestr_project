from flask import render_template, Blueprint
from main.models import User

primary = Blueprint('primary', __name__)

@primary.route("/")
def home():
    return render_template('home.html')

@primary.route("/about")
def about():
    users = User.query.all()
    return render_template('about.html', users=users)
