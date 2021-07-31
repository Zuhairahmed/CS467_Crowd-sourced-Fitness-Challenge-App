from wtforms import Form, StringField, PasswordField, validators, ValidationError
from wtforms.validators import InputRequired
from flask import flash


def flash_errors(form):
    """Flashes form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            flash(u"Error in the %s field - %s" % (
                getattr(form, field).label.text,
                error
            ), 'error')

def checkUsername(form, field):
    if len(field.data) < 4:
        raise ValidationError('Username must be at least 4 characters long.')
    if len(field.data) > 12:
        raise ValidationError('Username must be shorter than 12 characters.')


class RegistrationForm(Form):
    username = StringField('Username', [InputRequired(), checkUsername])
    password = PasswordField('New Password', [
        validators.DataRequired()
    ])
    firstname = StringField('First Name', [validators.data_required()])
    lastname = StringField('Last Name', [validators.data_required()])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
