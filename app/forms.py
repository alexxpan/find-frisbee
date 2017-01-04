from flask_wtf import Form
from wtforms import BooleanField, StringField, PasswordField, SubmitField, RadioField, validators, ValidationError

#Custom validators
def validate_date(form, field):
	#make sure date is in the format mm/dd
	months = ['01','02','03','04','05','06','07','08','09']
	for i in range(1, 12):
		months.append(str(i))
	days = ['01','02','03','04','05','06','07','08','09','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','28','29','30','31']
	if len(field.data) == 4:
		if field.data[0] in months and field.data[1] == '/' and field.data[2:4] in days:
			return 
	elif len(field.data) == 5:
		if field.data[0:2] in months and field.data[2] == '/' and field.data[3:5] in days:
			return 
	raise ValidationError('This field is either invalid or in the incorrect format (ex: 1/12 or 01/12).')

def validate_time(form, field):
	#make sure time is in the format hh:mm am/pm
	am_or_pm = ['am', 'pm']
	hours = ['1','2','3','4','5','6','7','8','9','01','02','03','04','05','06','07','08','09','10','11','12']
	minutes = ['00','01', '02', '03', '04', '05', '06', '07', '08', '09']
	for i in range(10, 60):
		minutes.append(str(i))
	if len(field.data) == 7:
		if field.data[0] in hours and field.data[1] == ':' and field.data[2:4] in minutes and field.data[4] == ' ' and field.data[5:7] in am_or_pm:
			return
	elif len(field.data) == 8:
		if field.data[0:2] in hours and field.data[2] == ':' and field.data[3:5] in minutes and field.data[5] == ' ' and field.data[6:8] in am_or_pm: 
			return
	raise ValidationError('This field is either invalid or in the incorrect format (ex: 5:23 pm, 10:20 am).')

#Forms
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
	date = StringField('Date', validators=[validators.DataRequired(), validate_date])
	location = StringField('Location', validators=[validators.DataRequired()])
	time = StringField('Time', validators=[validators.DataRequired(), validate_time])
	description = StringField('Description')

class GoingForm(Form):
	is_going = BooleanField('Is Going', default=False)
	confirm = SubmitField('Confirm')
	edit_event = SubmitField('Edit Event')

class EditEventForm(Form):
	new_type = StringField('Type')
	new_date = StringField('Date', validators=[validate_date])
	new_location = StringField('Location')
	new_time = StringField('Time', validators=[validate_time])
	new_description = StringField('Description')
	delete = BooleanField('Delete', default=False)



		








