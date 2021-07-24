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
        db.session.add(User(username=username, password=password, firstname=firstname, 
                            lastname=lastname, email=email, walloffame_id=None))
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
        db.session.add(User(username=username, password=password, firstname=firstname, 
                            lastname=lastname, email=email, walloffame_id=None))
        db.session.commit()
        return redirect(url_for('fitness_friends_challenge.index'))
    return render_template('registration.html')

# Route for user profile page
@bp.route('/users/<username>/profile', methods=('GET', 'POST'))
def userprofile(username):
    if request.method == 'POST':
        tag_name = request.form['name']
        tag = Tag.query.filter_by(name=tag_name).first()
        return redirect(url_for('fitness_friends_challenge.challenges', name=tag.name, username=username))
    user = User.query.filter_by(username=username).first()
    badges = Badge.query.filter(Badge.users.any(user=user)).all()
    tags = Tag.query.all()
    favorites = Favorites.query.filter_by(user_id=user.id).all()
    challenges = []
    for favorite in favorites:
        for challenge in Challenge.query.filter_by(favorites_id=favorite.id).all():
            challenges.append(challenge)
    return render_template('profile.html', user=user, badges=badges, tags=tags, challenges=challenges)

# Route for challenge search results page
@bp.route('/users/<username>/challenges/search/<name>', methods=('GET', 'POST'))
def challenges(username, name):
    if request.method == 'POST':
        challenge_name = request.form['challenge_name']
        challenge = Challenge.query.filter_by(name=challenge_name).first()
        user = User.query.filter_by(username=username).first()
        user_favorites = Favorites(user_id=user.id)
        user_favorites.challenges.append(challenge)
        db.session.add(user_favorites)
        db.session.commit()
        return redirect(url_for('fitness_friends_challenge.userprofile', username=username))
    tag = Tag.query.filter_by(name=name).first()
    challenges = Challenge.query.filter(Challenge.tags.any(name=tag.name)).all()
    return render_template('search.html', challenges=challenges, tag=tag)

# Route for create challenge page
@bp.route('/users/<username>/challenges/create', methods=('GET', 'POST'))
def createchallenge(username):
    if request.method == 'POST':
        user = User.query.filter_by(username=username).first()
        db.session.add(Favorites(user_id=user.id))
        db.session.commit()
        favorites = Favorites.query.filter_by(user_id=user.id).first()
        name = request.form['name']
        description = request.form['description']
        kind_name = request.form['kind']
        kind = Kind.query.filter_by(name=kind_name).first()
        tag_name = request.form['tag']
        tag = Tag.query.filter_by(name=tag_name).first()
        new_challenge = Challenge(name=name, description=description, favorites_id=favorites.id, kind_id=kind.id)
        new_challenge.tags.append(tag)
        db.session.add(new_challenge)
        db.session.commit()
        challenge = Challenge.query.filter_by(name=name).first()
        user_favorites = Favorites.query.filter_by(user_id=user.id).first()
        user_favorites.challenges.append(challenge)
        db.session.add(user_favorites)
        db.session.commit()
        update_fav = Favorites.query.filter_by(user_id=user.id).first()
        return redirect(url_for('fitness_friends_challenge.userprofile', username=username))
    tags = Tag.query.all()
    kinds = Kind.query.all()
    return render_template('create.html', tags=tags, kinds=kinds)

# Route for challenge home page
@bp.route('/challenges/<name>', methods=('GET', 'POST'))
def challengehome(name):
    if request.method == 'POST':
        challenge = Challenge.query.filter_by(name=name).first()
        return redirect(url_for('fitness_friends_challenge.walloffame', name=challenge.name))
    challenge = Challenge.query.filter_by(name=name).first()
    return render_template('challenge.html', challenge=challenge)

# Route for challenge wall of fame page
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