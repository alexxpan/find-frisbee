from flask_wtf import Form
from wtforms import BooleanField, StringField, PasswordField, SubmitField, RadioField, validators

class LoginForm(Form):
	email = StringField('Email Address', validators=[validators.DataRequired(), validators.Email()])
	password = PasswordField('Password', validators=[validators.DataRequired()])
	remember_me = BooleanField('Remember Me', default=False)

class SignupForm(Form):
	email = StringField('Email Address', validators=[validators.DataRequired(), validators.Email()])
	password = PasswordField('Password', validators=[validators.DataRequired()])
	confirm = PasswordField('Password', validators=[validators.EqualTo('password', message="Passwords do not match.")])
	nickname = StringField('Nickname', validators=[validators.DataRequired()])

class NicknameForm(Form):
	nickname = StringField('Nickname', validators=[validators.DataRequired()])

class PasswordForm(Form):
	old_password = PasswordField('Password', validators=[validators.DataRequired()])
	new_password = PasswordField('Password', validators=[validators.DataRequired()])
	new_confirm = PasswordField('Password', validators=[validators.EqualTo('new_password', message="Passwords do not match.")])

class EventForm(Form):
	type = StringField('Type', validators=[validators.DataRequired()])
	date = StringField('Date', validators=[validators.DataRequired()])
	location = StringField('Location', validators=[validators.DataRequired()])
	time = StringField('Time', validators=[validators.DataRequired()])
	description = StringField('Description')

class GoingForm(Form):
	is_going = BooleanField('Is Going', default=False)
	confirm = SubmitField('Confirm')
	edit_event = SubmitField('Edit Event')

class EditEventForm(Form):
	new_type = StringField('Type')
	new_date = StringField('Date')
	new_location = StringField('Location')
	new_time = StringField('Time')
	new_description = StringField('Description')
	delete = BooleanField('Delete', default=False)











