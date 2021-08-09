import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

BASEDIRECTORY = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = BASEDIRECTORY + '/static/images'
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev_key',
        UPLOAD_FOLDER = UPLOAD_FOLDER,
        SQLALCHEMY_DATABASE_URI = 'postgresql://jcqomyoeuvlwiy:6bd0835cfb0797bb13ef0e4548928c06d8cdb0a79b051d70312a9aea1356ba7a@ec2-54-224-194-214.compute-1.amazonaws.com:5432/d1rvvqpp8hfonq',
        SQLALCHEMY_TRACK_MODIFICATIONS = False
    )

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'index'

    from . import models
    from . import forms
    from . import fitness_friends_challenge
    app.register_blueprint(fitness_friends_challenge.bp)

    return app