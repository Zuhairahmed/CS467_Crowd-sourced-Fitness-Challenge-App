import re
from flask import flash
from wtforms import Form, StringField, PasswordField, validators, ValidationError
from wtforms.validators import InputRequired, email, email_validator
from fitness_friends_challenge.models import User


def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')


def username_taken_check(form, user_name):
    taken = User.query.filter_by(username=user_name.data).first()
    if taken:
        raise ValidationError('That username is taken. Please choose another.')


def email_taken_check(form, user_email):
    taken = User.query.filter_by(email=user_email.data).first()
    if taken:
        raise ValidationError('That email is taken. Please choose another.')


def checkUsername(form, username):
    if len(username.data) < 4:
        raise ValidationError('Username must be at least 4 characters long.')
    if len(username.data) > 12:
        raise ValidationError('Username must be shorter than 12 characters.')


def checkPassword(form, field):
    if len(field.data) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    elif len(field.data) > 32:
        raise ValidationError("Password can't be bigger than 32 characters long.")
    elif re.search('[0-9]', field.data) is None:
        raise ValidationError("Your password must have a number in it.")
    elif re.search('[A-Z]', field.data) is None:
        raise ValidationError("Your password must have a capital letter in it.")


class RegistrationForm(Form):
    username = StringField('Username',
                           [InputRequired(message="Please enter a username"), validators.Length(min=3, max=10),
                            checkUsername, username_taken_check])
    password = PasswordField('New Password',
                             [validators.DataRequired(message="Please enter a password."), checkPassword])
    firstname = StringField('First Name', [validators.data_required()])
    lastname = StringField('Last Name', [validators.data_required()])
    email = StringField('Email Address', [email(), validators.Length(min=6, max=35), email_taken_check])
