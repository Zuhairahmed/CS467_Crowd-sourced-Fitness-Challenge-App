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
        user = User.query.filter_by(username=username).first()
        if user.password == password:
            return redirect(url_for('fitness_friends_challenge.userprofile', username=user.username))
    return render_template('index.html')

# Admin page to create and review created users 
@bp.route('/users', methods=('GET', 'POST'))
def users():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        db.session.add(User(username=username, password=password, firstname=firstname, lastname=lastname,
                            email=email, walloffame_id=None))
        db.session.commit()
    users = User.query.all()
    return render_template('users.html', users=users)

# Admin page to create and review created tags 
@bp.route('/tags', methods=('GET', 'POST'))
def tags():
    if request.method == 'POST':
        name = request.form['name']
        db.session.add(Tag(name=name))
        db.session.commit()
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

# Admin page to create and review created badges 
@bp.route('/badges', methods=('GET', 'POST'))
def badges():
    if request.method == 'POST':
        image = request.form['image']
        db.session.add(Badge(image=image))
        db.session.commit()
    badges = Badge.query.all()
    return render_template('badges.html', badges=badges)

# Admin page to create and review created kind of challenges 
@bp.route('/kinds', methods=('GET', 'POST'))
def kinds():
    if request.method == 'POST':
        name = request.form['name']
        db.session.add(Kind(name=name))
        db.session.commit()
    kinds = Kind.query.all()
    return render_template('kinds.html', kinds=kinds)

# Route for user registration page
@bp.route('/registration', methods=('GET', 'POST'))
def registration():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        db.session.add(User(username=username, password=password, firstname=firstname, lastname=lastname,
                            email=email, walloffame_id=None))
        db.session.commit()
        return redirect(url_for('index.html'))
    return render_template('registration.html')

# Route for user profile page
@bp.route('/users/<username>/profile', methods=('GET', 'POST'))
def userprofile(username):
    user = User.query.filter_by(username=username).first()
    return render_template('profile.html', user=user)

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
@bp.route('/challenges/<name>')
def challengehome(name):
    return render_template('challenge.html')

# Route for challenge wall of fame page
# Note: this route's url will change to include challenge name when set up
@bp.route('/challenges/<name>/wall-of-fame')
def walloffame(name):
    return render_template('wall.html')

# Route for about us page
@bp.route('/about-us')
def about():
    return render_template('about.html')

# Route for faq page
@bp.route('/learn-more')
def faq():
    return render_template('faq.html')