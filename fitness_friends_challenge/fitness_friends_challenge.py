###############################################################################
#
# Authors: Bryan DiStefano, Bryce Koenig, Zuhair Ahmed
# Course: OSU CS467_400_Summer 2021
#
# Description:
# Friends Fitness Challenge is a crowd-sources fitness challenge cross-platform web application for Web and Mobile (Android)
# Users have their own accounts and then are able to create and participate in user created fitness challenges.
#
# References:
# https://flask.palletsprojects.com/en/2.0.x/tutorial/index.html
# https://docs.sqlalchemy.org/en/14/orm/tutorial.html
# https://www.youtube.com/watch?v=2e4STDACVA8
# https://devcenter.heroku.com/articles/flask-memcache#create-a-flask-application-for-heroku
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/
# https://flask-migrate.readthedocs.io/en/latest/
# https://flask-login.readthedocs.io/en/latest/
# https://flask.palletsprojects.com/en/2.0.x/patterns/fileuploads/
#
###############################################################################
import os
from flask import Flask, redirect, render_template, request, url_for, Blueprint, flash, current_app
from flask_login import login_user, login_required, logout_user, login_fresh, current_user
from fitness_friends_challenge import db
from fitness_friends_challenge.models import Challenge, User, Badge, Favorites, Tag, Goal, Chat, Image, WallOfFame, Kind, Progress
from fitness_friends_challenge.forms import RegistrationForm, flash_errors
from werkzeug.utils import secure_filename


ALLOWED_EXTENSIONS = {'jpg', 'JPG', 'jpeg', 'png', '.PNG'}
bp = Blueprint('fitness_friends_challenge', __name__)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@bp.app_errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@bp.app_errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Route handles logging out user
@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged Out')
    return redirect(url_for('fitness_friends_challenge.index'))

# Default route displays Home/Landing page
@bp.route('/', methods=('GET', 'POST'))
def index():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is not None and User.check_password(user, password):
            login_user(user)
            return redirect(url_for('fitness_friends_challenge.userprofile', username=user.username))
        else:
            if user is None:
                flash('User with that User Name does not exist')
            else:
                flash('Invalid Password for User')
    if login_fresh() and current_user.is_authenticated:
        return redirect(url_for('fitness_friends_challenge.userprofile', 
            username=current_user.username))
    return render_template('index.html')

# Admin page to create and review created users
@bp.route('/users', methods=('GET', 'POST'))
@login_required
def users():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        db.session.add(User(username=username, password=password, firstname=firstname, 
                            lastname=lastname, email=email))
        db.session.commit()
    users = User.query.all()
    return render_template('users.html', users=users)

# Admin page to create and review created tags
@bp.route('/tags', methods=('GET', 'POST'))
@login_required
def tags():
    if request.method == 'POST':
        name = request.form['name']
        db.session.add(Tag(name=name))
        db.session.commit()
    tags = Tag.query.all()
    return render_template('tags.html', tags=tags)

# Admin page to create and review created badges
@bp.route('/badges', methods=('GET', 'POST'))
@login_required
def badges():
    if request.method == 'POST':
        image = request.form['image']
        db.session.add(Badge(image=image))
        db.session.commit()
    badges = Badge.query.all()
    return render_template('badges.html', badges=badges)

# Admin page to create and review created kind of challenges
@bp.route('/kinds', methods=('GET', 'POST'))
@login_required
def kinds():
    if request.method == 'POST':
        name = request.form['name']
        db.session.add(Kind(name=name))
        db.session.commit()
    kinds = Kind.query.all()
    return render_template('kinds.html', kinds=kinds)

# Admin page to create and review created kind of challenges
@bp.route('/images', methods=('GET', 'POST'))
@login_required
def images():
    if request.method == 'POST':
        name = request.form['name']
        admin_user = User.query.filter_by(username='Admin').first()
        db.session.add(Image(name=name, user_id=admin_user.id))
        db.session.commit()
        image = Image.query.filter_by(name=name).first()
        user = User.query.filter_by(username='Admin').first()
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
                            lastname=lastname, email=email))
        db.session.commit()
        flash('You are now registered and can Log In!')
        return redirect(url_for('fitness_friends_challenge.index'))
    else:
        flash_errors(form)
    return render_template('registration.html', form=form)

# Route for uploading of user images
@bp.route('/users/<username>/upload', methods=('GET', 'POST'))
def upload(username):
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file was chosen for upload')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file was selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            if Image.query.filter_by(name=filename).first() is None:
                file.save(os.path.join(current_app.config['UPLOAD_FOLDER'], filename))
                user = User.query.filter_by(username=username).first()  
                db.session.add(Image(name=filename, user_id=user.id))
                db.session.commit()
                image = Image.query.filter_by(name=filename).first()
                user.images.append(image)
                db.session.add(user)
                db.session.commit()
                flash('User image uploaded successfully')
                return redirect(url_for('fitness_friends_challenge.userprofile', username=username))
            else:
                flash('User image already exists, upload different image')
                return redirect(request.url)
        else:
            flash('Uploaded file is not secure, choose another image')
            return redirect(request.url)
    return render_template('upload.html')

# Route for user profile page
@bp.route('/users/<username>/profile', methods=('GET', 'POST'))
@login_required
def userprofile(username):
    if request.method == 'POST':
        tag_name = request.form['name']
        tag = Tag.query.filter_by(name=tag_name).first()
        return redirect(url_for('fitness_friends_challenge.challenges', name=tag.name, username=username))
    user = User.query.filter_by(username=username).first()
    earned_badges = Badge.query.filter(Badge.users.any(username=user.username)).all()
    tags = Tag.query.all()
    favorites = Favorites.query.filter_by(user_id=user.id).all()
    images = Image.query.filter_by(user_id=user.id).all()
    challenges = []
    for favorite in favorites:
        for challenge in Challenge.query.filter_by(favorites_id=favorite.id).all():
            challenges.append(challenge)
    return render_template('profile.html', earned_badges=earned_badges, tags=tags, 
                           challenges=challenges, images=images)

# Route for challenge search results page
@bp.route('/users/<username>/challenges/search/<name>', methods=('GET', 'POST'))
@login_required
def challenges(username, name):
    if request.method == 'POST':
        challenge_name = request.form['challenge_name']
        challenge = Challenge.query.filter_by(name=challenge_name).first()
        user = User.query.filter_by(username=username).first()
        user_favorites = Favorites(user_id=user.id)
        user_favorites.challenges.append(challenge)
        db.session.add(user_favorites)
        db.session.commit()
        challenge_goal = Goal.query.filter_by(challenge_id=challenge.id).first()
        db.session.add(Progress(first_goal_progress=0, second_goal_progress=0, third_goal_progress=0,
                                user_id=user.id, goal_id=challenge_goal.id))
        db.session.commit()
        user_progress = Progress.query.filter_by(user_id=user.id).first()
        user.goals_progress.append(user_progress)
        db.session.add(user)
        db.session.commit()
        db.session.add(user_progress)
        db.session.commit()
        goal_progress = Progress.query.filter_by(goal_id=challenge_goal.id).first()
        challenge_goal.progresses.append(goal_progress)
        db.session.add(challenge_goal)
        db.session.commit()
        return redirect(url_for('fitness_friends_challenge.userprofile', username=username))
    tag = Tag.query.filter_by(name=name).first()
    challenges = Challenge.query.filter(Challenge.tags.any(name=tag.name)).all()
    return render_template('search.html', challenges=challenges, tag=tag)

# Route for create challenge page
@bp.route('/users/<username>/challenges/create', methods=('GET', 'POST'))
@login_required
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
                                user_id=user.id, goal_id=goal.id))
        db.session.commit()
        user_progress = Progress.query.filter_by(user_id=user.id).first()
        user.goals_progress.append(user_progress)
        db.session.add(user)
        db.session.commit()
        db.session.add(user_progress)
        db.session.commit()
        goal_progress = Progress.query.filter_by(goal_id=goal.id).first()
        goal.progresses.append(goal_progress)
        db.session.add(goal)
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
@login_required
def challengehome(username, name):
    challenge = Challenge.query.filter_by(name=name).first()
    user = User.query.filter_by(username=username).first()
    goal = Goal.query.filter_by(challenge_id=challenge.id).first()
    goal_progress = Progress.query.filter_by(goal_id=goal.id).first()
    user_goals_progress = Progress.query.filter_by(user_id=user.id).all()
    print(f'user_goals_progress are {user_goals_progress}')
    for user_progress in user_goals_progress:
        print(f'user_progress is {user_progress}')
        print(f'user_progress.id is {user_progress.id}')
        print(f'goal_progress.id is {goal_progress.id}')
        print(f'user_progress.goal_id is {user_progress.goal_id}')
        print(f'goal_progress.goal_id is {goal_progress.goal_id}')
        print(f'user_progress.user_id is {user_progress.user_id}')
        print(f'goal_progress.user_id is {goal_progress.user_id}')
        if user_progress.goal_id == goal_progress.goal_id and user_progress.user_id == goal_progress.user_id:
            progress = user_progress
            print(f'progress is {progress}')
    if request.method == 'POST':
        print(f'progress.user_id in post is {progress.user_id}')
        print(f'progress.goal_id in post is {progress.goal_id}')
        first_goal_progress = request.form['first_goal_progress']
        second_goal_progress = request.form['second_goal_progress']
        third_goal_progress = request.form['third_goal_progress']
        if first_goal_progress != '':
            progress.first_goal_progress = int(first_goal_progress)
        if second_goal_progress != '':
            progress.second_goal_progress = int(second_goal_progress)
        if third_goal_progress != '':
            progress.third_goal_progress = int(third_goal_progress)
            if int(third_goal_progress) >= goal.third_target_number:
                walloffame = WallOfFame.query.filter_by(challenge_id=challenge.id).first()
                user.walloffame_id = walloffame.id
                user.challenges_completed = user.challenges_completed + 1
                if user.challenges_completed > 1:
                    earned_badge = None
                    found_unearned_badge = False
                    challenge_badges_available = Badge.query.filter(
                        Badge.challenges.any(name=challenge.name)).all()
                    user_badges_earned = Badge.query.filter(Badge.users.any(username=user.username)).all()
                    for challenge_badge in challenge_badges_available:
                        if found_unearned_badge == False:
                            badge = Badge.query.filter_by(image=challenge_badge.image).first()
                            if user_badges_earned != []:
                                for user_badge in user_badges_earned:
                                    if challenge_badge.image == user_badge.image:
                                        continue
                                    else:
                                        earned_badge = badge
                                        found_unearned_badge = True
                                        break
                            else:
                                earned_badge = badge
                                found_unearned_badge = True
                        else:
                            user.badges.append(earned_badge)
                            break
                    earned_badge.users.append(user)
                    db.session.add(earned_badge)
                    db.session.commit()
                db.session.add(user)
                db.session.commit()
                user_add_to_wall = User.query.filter_by(username=username).first()
                walloffame.users.append(user_add_to_wall)
                db.session.add(walloffame)
                db.session.commit()
        db.session.add(user_progress)
        db.session.commit()
        return redirect(url_for('fitness_friends_challenge.challengehome', username=username, name=name))
    challenge_image_by_creator = challenge.images[0] 
    print(f'challenge_images_by_creator before check is {challenge_image_by_creator}')
    print(f'user.images are {user.images}')
    for user_image in user.images:
        print(f'user_image is {user_image}')
        for challenge_image in challenge.images:
            print(f'challenge_image is {challenge_image}')
            print(f'user_image.name is {user_image.name}')
            print(f'challenge_image.name is {challenge_image.name}')
            if user_image.name == challenge_image.name:
                challenge_image_by_creator = challenge_image.name
                print(f'challenge_image_by_creator after assignment is {challenge_image_by_creator}')
    challenge_badges = []
    for badge in challenge.badges:
        challenge_badges.append(badge.image)
    challenge_incomplete = True
    print(f'in get before progress and it is {progress}')
    print(f'its user_id is {progress.user_id}')
    print(f'its goal_id is {progress.goal_id}')
    print(f'value of challenge_incomplete is {challenge_incomplete}')
    print(f'progress.third_goal_progress is {progress.third_goal_progress}')
    print(f'goal.third_target_number is {goal.third_target_number}')
    if progress.third_goal_progress >= goal.third_target_number:
        challenge_incomplete = False
    return render_template('challenge.html', challenge=challenge, challenge_image=challenge_image_by_creator,
                            challenge_badges=challenge_badges, goal=goal, progress=progress,
                            challenge_incomplete=challenge_incomplete)

# Route for challenge wall of fame page
@bp.route('/users/<username>/challenges/<name>/wall-of-fame')
@login_required
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

# Route for weather page
@bp.route('/weather')
def weather():
    return render_template('weather.html')

# Route for map page
@bp.route('/map')
def map():
    return render_template('map.html')

# Route for social page
@bp.route('/social')
def social():
    return render_template('social.html')

# Route for radio page
@bp.route('/radio')
def radio():
    return render_template('radio.html')