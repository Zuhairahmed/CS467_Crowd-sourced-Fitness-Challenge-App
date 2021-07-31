from wtforms import Form, StringField, PasswordField, validators, ValidationError
from wtforms.validators import InputRequired, email, email_validator
from flask import flash
import re


def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')

def checkPassword(form, field):
    if len(field.data) < 8:
        raise ValidationError("Password must be at least 8 characters long.")
    elif len(field.data) > 32:
        raise ValidationError("Password can't be bigger than 32 characters long.")
    elif re.search('[0-9]',field.data) is None:
        raise ValidationError("Your password must have a number in it.")
    elif re.search('[A-Z]',field.data) is None:
        raise ValidationError("Your password must have a capital letter in it.")






class RegistrationForm(Form):
    username = StringField('Username', [InputRequired(message="Please enter a username"), validators.Length(min=3, max=10)])
    password = PasswordField('New Password', [validators.DataRequired(message="Please enter a password."), checkPassword])
    firstname = StringField('First Name', [validators.data_required()])
    lastname = StringField('Last Name', [validators.data_required()])
    email = StringField('Email Address', [email(), validators.Length(min=6, max=35)])




