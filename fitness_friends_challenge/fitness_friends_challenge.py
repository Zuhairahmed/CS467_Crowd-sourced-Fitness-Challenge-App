from flask import Flask, redirect, render_template, request, url_for, session, Blueprint
from fitness_friends_challenge import db
from fitness_friends_challenge.models import Challenge

bp = Blueprint('fitness_friends_challenge', __name__)

#Default route displays index page
@bp.route('/')
def index():
    return render_template('index.html')