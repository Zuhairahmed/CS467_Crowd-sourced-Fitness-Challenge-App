###############################################################################
#
# Authors: Bryan DiStefano, Bryce Koenig, Zuhair Ahmed
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
from fitness_friends_challenge.models import Challenge, User, Badge, Favorites, Tag, Goal, Chat, Image, WallOfFame, Kind, Progress
from fitness_friends_challenge.forms import RegistrationForm, flash_errors


bp = Blueprint('fitness_friends_challenge', __name__)

@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@bp.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

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
                            lastname=lastname, email=email, walloffame_id=None, challenges_completed=0))
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

# Admin page to create and review created kind of challenges 
@bp.route('/images', methods=('GET', 'POST'))
def images():
    if request.method == 'POST':
        name = request.form['name']
        db.session.add(Image(name=name, user_id=1))
        db.session.commit()
        image = Image.query.filter_by(name=name).first()
        user = User.query.get(1)
        user.images.append(image)
        db.session.add(user)
        db.session.commit()
    images = Image.query.all()
    return render_template('image.html', images=images)

# Route for user registration page
@bp.route('/registration', methods=('GET', 'POST'))
def registration():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        db.session.add(User(username=username, password=password, firstname=firstname, 
                            lastname=lastname, email=email, walloffame_id=None, challenges_completed=0))
        db.session.commit()
        return redirect(url_for('fitness_friends_challenge.index'))
    else:
        flash_errors(form)
    return render_template('registration.html', form=form)

# Route for user profile page
@bp.route('/users/<username>/profile', methods=('GET', 'POST'))
def userprofile(username):
    if request.method == 'POST':
        tag_name = request.form['name']
        tag = Tag.query.filter_by(name=tag_name).first()
        return redirect(url_for('fitness_friends_challenge.challenges', name=tag.name, username=username))
    user = User.query.filter_by(username=username).first()
    earned_badges = Badge.query.filter(Badge.users.any(user=user)).all()
    tags = Tag.query.all()
    favorites = Favorites.query.filter_by(user_id=user.id).all()
    challenges = []
    for favorite in favorites:
        for challenge in Challenge.query.filter_by(favorites_id=favorite.id).all():
            challenges.append(challenge)
    return render_template('profile.html', user=user, earned_badges=earned_badges, tags=tags, 
                           challenges=challenges)

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
        challenge_name = request.form['challenge_name']
        description = request.form['challenge_description']
        kind_name = request.form['kind']
        kind = Kind.query.filter_by(name=kind_name).first()
        goal_name = request.form['goal_name']
        first_goal_step = request.form['first_target_number']
        second_goal_step = request.form['second_target_number']
        third_goal_step = request.form['third_target_number']
        db.session.add(Goal(name=goal_name, first_target_number=first_goal_step, 
                            second_target_number=second_goal_step,
                            third_target_number=third_goal_step, challenge_id=None))
        db.session.commit()
        goal = Goal.query.filter_by(name=goal_name).first()
        image_name = request.form['image']
        image = Image.query.filter_by(name=image_name).first()
        tag_names = request.form.getlist('tags')
        tags_added = []
        badges_names = request.form.getlist('badges')
        badges_added = []
        for tag_name in tag_names:
            tag = Tag.query.filter_by(name=tag_name).first()
            tags_added.append(tag)
        for badge_name in badges_names:
            badge = Badge.query.filter_by(image=badge_name).first()
            badges_added.append(badge)
        new_challenge = Challenge(name=challenge_name, description=description, creator=username, 
                                favorites_id=favorites.id, kind_id=kind.id)
        new_challenge.images.append(image)
        new_challenge.goals.append(goal)
        for tag in tags_added:
            new_challenge.tags.append(tag)
        for badge in badges_added:
            new_challenge.badges.append(badge)
        db.session.add(new_challenge)
        db.session.commit()
        challenge = Challenge.query.filter_by(name=challenge_name).first()
        db.session.add(WallOfFame(challenge_id=challenge.id))
        db.session.commit()
        walloffame = WallOfFame.query.filter_by(challenge_id=challenge.id).first()
        challenge.walloffames.append(walloffame)
        db.session.add(challenge)
        db.session.commit()
        goal.challenge_id = challenge.id
        db.session.add(Progress(first_goal_progress=0, second_goal_progress=0, third_goal_progress=0,
                                user_id=user.id))
        db.session.commit()
        progress = Progress.query.filter_by(user_id=user.id).first()
        user.goals_progress.append(progress)
        db.session.add(user)
        db.session.commit()
        goal.progress_id = progress.id
        db.session.add(goal)
        db.session.commit()
        progress.goals.append(goal)
        db.session.add(progress)
        db.session.commit()
        challenge_tags = []
        for tag in tags_added:
            challenge_tags.append(Tag.query.filter_by(name=tag.name).first())
        for challenge_tag in challenge_tags:
            challenge_tag.challenges.append(challenge)
        challenge_badges = []
        for badge in badges_added:
            challenge_badges.append(Badge.query.filter_by(image=badge.image).first())
        for challenge_badge in challenge_badges:
            challenge_badge.challenges.append(challenge)
        user_favorites = Favorites.query.filter_by(user_id=user.id).first()
        user_favorites.challenges.append(challenge)
        image.challenges.append(challenge)
        db.session.add(image)
        db.session.commit()
        db.session.add(user_favorites)
        db.session.commit()
        for tag in challenge_tags:
            db.session.add(tag)
            db.session.commit()
        for badge in challenge_badges:
            db.session.add(badge)
            db.session.commit()
        return redirect(url_for('fitness_friends_challenge.userprofile', username=username))
    user = User.query.filter_by(username=username).first()
    tags = Tag.query.all()
    kinds = Kind.query.all()
    badges = Badge.query.all()
    images = Image.query.filter_by(user_id=user.id).all()
    return render_template('create.html', tags=tags, kinds=kinds, badges=badges, images=images)

# Route for challenge home page
@bp.route('/users/<username>/challenges/<name>', methods=('GET', 'POST'))
def challengehome(username, name):
    if request.method == 'POST':
        first_goal_progress = int(request.form['first_goal_progress'])
        second_goal_progress = int(request.form['second_goal_progress'])
        third_goal_progress = int(request.form['third_goal_progress'])
        challenge = Challenge.query.filter_by(name=name).first()
        user = User.query.filter_by(username=username).first()
        user_progress = Progress.query.filter_by(user_id=user.id).first()
        if first_goal_progress:
            user_progress.first_goal_progress = first_goal_progress
        if second_goal_progress:
            user_progress.second_goal_progress = second_goal_progress
        if third_goal_progress:
            user_progress.third_goal_progress = third_goal_progress
            goal = Goal.query.filter_by(challenge_id=challenge.id).first()
            if goal.third_target_number - third_goal_progress == 0:
                walloffame = WallOfFame.query.filter_by(challenge_id=challenge.id).first()
                user.walloffame_id = walloffame.id
                user.challenges_completed = user.challenges_completed + 1
                if user.challenges_completed > 1:
                    challenge_badges_available = Badge.query.filter(
                        Badge.challenges.any(name=challenge.name).all())
                    for challenge_badge in challenge_badges_available:
                        for user_badge in user.badges:
                            if challenge_badge.image != user_badge.image:
                                user.badges.append(challenge_badge)
                db.session.add(user)
                db.session.commit()
                user_add_to_wall = User.query.filter_by(username=username).first()
                walloffame.users.append(user_add_to_wall)
                db.session.add(walloffame)
                db.session.commit()
        db.session.add(user_progress)
        db.session.commit()
    challenge = Challenge.query.filter_by(name=name).first()
    user = User.query.filter_by(username=username).first()
    for user_image in user.images:
        for challenge_image in challenge.images:
            if user_image.name == challenge_image.name:
                challenge_image_by_creator = challenge_image.name
    challenge_badges = []
    for badge in challenge.badges:
        challenge_badges.append(badge.image)
    goal = Goal.query.filter_by(challenge_id=challenge.id).first()
    progress = Progress.query.filter_by(user_id=user.id).first()
    challenge_incomplete = True
    if goal.third_target_number - progress.third_goal_progress == 0:
        challenge_incomplete = False
    return render_template('challenge.html', challenge=challenge, challenge_image=challenge_image_by_creator,
                            challenge_badges=challenge_badges, goal=goal, user=user, progress=progress,
                            challenge_incomplete=challenge_incomplete)

# Route for challenge wall of fame page
@bp.route('/users/<username>/challenges/<name>/wall-of-fame')
def walloffame(username, name):
    challenge = Challenge.query.filter_by(name=name).first()
    challenge_walloffame = WallOfFame.query.filter_by(challenge_id=challenge.id).first()
    return render_template('wall.html', users=challenge_walloffame.users, challenge=challenge)

# Route for about us page
@bp.route('/about-us')
def about():
    return render_template('about.html')

# Route for faq page
@bp.route('/learn-more')
def faq():
    return render_template('faq.html')





