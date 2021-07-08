from flask import Flask, redirect, render_template, request, url_for, session, Blueprint
from fitness_friends_challenge import db
from fitness_friends_challenge.models import Challenge

bp = Blueprint('fitness_friends_challenge', __name__)

#Default route displays Home/Landing page
@bp.route('/')
def index():
    return render_template('index.html')

#Route for user registration page
@bp.route('/registration')
def registration():
    return render_template('registration.html')

#Route for user profile page
#Note: this route's url will change to the username once logged in, when that is set up
@bp.route('/usernamehere/profile')
def userprofile():
    return render_template('profile.html')

#Route for challenge search results page
#Note: this route's url will change to include tags used for search when set up
@bp.route('/challenges/search')
def challenges():
    return render_template('search.html')

#Route for create challenge page
@bp.route('/challenges/create')
def createchallenge():
    return render_template('create.html')

#Route for challenge home page
#Note: this route's url will change to include challenge name when set up
@bp.route('/challenges/challengenamehere')
def challengehome():
    return render_template('challenge.html')

#Route for challenge wall of fame page
#Note: this route's url will change to include challenge name when set up
@bp.route('/challenges/challengenamehere/wall-of-fame')
def walloffame():
    return render_template('wall.html')

#Route for about us page
@bp.route('/about-us')
def about():
    return render_template('about.html')

#Route for faq page
@bp.route('/learn-more')
def faq():
    return render_template('faq.html')