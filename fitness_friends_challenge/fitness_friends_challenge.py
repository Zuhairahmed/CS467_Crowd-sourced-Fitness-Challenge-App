###############################################################################
#
# Authors: Brian DiStefano, Bryce Koenig, Zuhair Ahmed
# Course: CS467_400_Summer 2021
#
# Description:
# TBD
#
# References:
# TBD1
# TBD2
# TBD3
#
###############################################################################

from flask import Flask, redirect, render_template, request, url_for, session, Blueprint, flash
from fitness_friends_challenge import db
from fitness_friends_challenge.models import Challenge, User, Badge, Favorites, Tag, Goal, Chat, Image, WallOfFame, Kind


bp = Blueprint('fitness_friends_challenge', __name__)


# Default route displays Home/Landing page
@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        if not username:
            flash('User info is required.')
        else:
            db.session.add(User(username=username, password=password, firstname=firstname, lastname=lastname,
                                email=email))
            db.session.commit()

    users = User.query.all()
    return render_template('index.html', users=users)


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        if not username:
            flash('User info is required.')
        else:
            db.session.add(User(username=username, password=password, firstname=firstname, lastname=lastname,
                                email=email))
            db.session.commit()

    users = User.query.all()
    return render_template('login.html', users=users)

# Route for user registration page


@bp.route('/registration')
def registration():
    return render_template('registration.html')

# Route for user profile page
# Note: this route's url will change to the username once logged in, when that is set up


@bp.route('/usernamehere/profile')
def userprofile():
    return render_template('profile.html')

# Route for challenge search results page
# Note: this route's url will change to include tags used for search when set up


@bp.route('/challenges/search')
def challenges():
    return render_template('search.html')

# Route for create challenge page


@bp.route('/challenges/create')
def createchallenge():
    return render_template('create.html')

# Route for challenge home page
# Note: this route's url will change to include challenge name when set up


@bp.route('/challenges/challengenamehere')
def challengehome():
    return render_template('challenge.html')

# Route for challenge wall of fame page
# Note: this route's url will change to include challenge name when set up


@bp.route('/challenges/challengenamehere/wall-of-fame')
def walloffame():
    return render_template('wall.html')

# Route for about us page


@bp.route('/about-us')
def about():
    return render_template('about.html')

# Route for faq page


@bp.route('/learn-more')
def faq():
    return render_template('faq.html')
