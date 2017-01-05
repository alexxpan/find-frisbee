from flask import render_template, flash, redirect, session, url_for, request, g, Markup
from app import app, db, lm
from .forms import LoginForm, SignupForm, NicknameForm, PasswordForm, EventForm, GoingForm, EditEventForm
from flask_login import login_user, logout_user, current_user, login_required
from .models import User, Event
from datetime import datetime

@app.before_request
def before_request():
	g.user = current_user

@lm.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.route('/')
@app.route('/landing')
def landing():
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('index'))
	return render_template('landing.html')

@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
	user = g.user
	events = Event.query.all()
	#change formatting for event date and time
	for event in events:
		#change time to correct format (hh:mm in 24-hr format)
		formatted_time = event.time
		if len(event.time) == 7:
			formatted_time = '0' + formatted_time
		if formatted_time[6:8] == 'pm':
			hour = int(formatted_time[0:2]) + 12 
			formatted_time = str(hour) + formatted_time[2:]
		formatted_time = formatted_time[0:5]
		event.formatted_time = formatted_time
		#change date to correct format (mm/dd)
		formatted_date = event.date
		if len(event.date) == 4:
			formatted_date = '0' + formatted_date
		event.formatted_date = formatted_date
	#sort events by date and time
	events.sort(key=lambda x: x.formatted_date + x.formatted_time)
	#don't display events on days that have already passed
	current_date = datetime.now().strftime('%m/%d')
	for event in events:
		if event.formatted_date < current_date:
			events.remove(event)
	forms = []
	#create a form for each event to mark attendance (or to edit event if host)
	for i in range(len(events)):
		forms.append(GoingForm(prefix="form%s" % i))
	for i in range(len(forms)):
		#redirect to event edit page if 'edit event' is pressed
		if forms[i].validate_on_submit() and forms[i].edit_event and events[i].host_id == user.id:
			return redirect(url_for('editevent', event_id = events[i].id))
		#change event attendance status if it is different from before
		elif forms[i].validate_on_submit() and forms[i].confirm:
			if forms[i].is_going.data and events[i] not in user.events:
				user.events.append(events[i])
				db.session.commit()
				flash('You are now attending %s' % events[i].type)
				return redirect(url_for('index'))
			elif not forms[i].is_going.data and events[i] in user.events:
				user.events.remove(events[i])
				db.session.commit()
				flash('You are no longer attending %s' % events[i].type)
				return redirect(url_for('index'))
	return render_template('index.html',
						   title='Cal',
						   user=user,
						   events=events,
						   forms=forms)

@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	#redirect to home page if already logged in
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('index'))
	if form.validate_on_submit():
		session['remember_me'] = form.remember_me.data
		user = User.query.filter_by(email=form.email.data).first()
		#check if valid user
		if user is None:
			message = Markup('No account associated with given email address. Please try again or sign up <a href="/signup">here</a>.')
			flash(message)
			return redirect(url_for('login'))
		#check password
		if user.password != form.password.data:
			flash('Incorrect password. Please try again.')
			return redirect(url_for('login'))
		remember_me = False
		if 'remember_me' in session:
			remember_me = session['remember_me']
			session.pop('remember_me', None)
		login_user(user, remember = remember_me)
		return redirect(url_for('index'))
	return render_template('login.html',
							form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()
	#redirect to home page if already logged in
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('index'))
	if form.validate_on_submit():
		#check if user already exists
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None:
			message = Markup('An account already exists for the given email address. Please try again or log in <a href="/login">here</a>.')
			flash(message)
			return redirect(url_for('signup'))
		#create a new user and add to database
		user = User(nickname=form.nickname.data, email=form.email.data, password=form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Account creation success. Please log in below.')
		return redirect(url_for('login'))
	return render_template('signup.html',
							form=form)

@app.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('landing'))

@app.route('/profile/<user_id>')
def profile(user_id):
	user = User.query.filter_by(id=user_id).first()
	if user == None:
		flash('User %s not found.' % user_id)
		return redirect(url_for('index'))
	return render_template('profile.html',
							user=user)

@app.route('/changenickname', methods=['GET', 'POST'])
@login_required
def changenickname():
	form = NicknameForm()
	user = g.user
	if form.validate_on_submit():
		flash('Nickname successfully changed.')
		user.nickname = form.nickname.data
		db.session.commit()
		return redirect(url_for('profile', user_id = user.id))
	return render_template('changenickname.html',
							form=form)

@app.route('/changepassword', methods=['GET', 'POST'])
@login_required
def changepassword():
	form = PasswordForm()
	user = g.user
	if form.validate_on_submit():
		if user.password == form.old_password.data:
			flash('Password successfully changed.')
			user.password = form.new_password.data
			db.session.commit()
			return redirect(url_for('profile', user_id = user.id))
		flash('Error: Old password does not match current password.')
		return redirect(url_for('changepassword'))
	return render_template('changepassword.html',
							form=form)

@app.route('/createevent', methods=['GET', 'POST'])
@login_required
def createevent():
	form = EventForm()
	user = g.user
	if form.validate_on_submit():
		#create new event and add to database
		event = Event(type=form.type.data, date=form.date.data, location=form.location.data, time=form.time.data, description=form.description.data, host_id=user.id, going=[user])
		db.session.add(event)
		user.events.append(event)
		db.session.commit()
		flash('Your event is now live! Tell your friends about it!')
		return redirect(url_for('index'))
	return render_template('event.html',
							form=form)

@app.route('/editevent/<event_id>', methods=['GET', 'POST'])
@login_required
def editevent(event_id):
	user = g.user
	form = EditEventForm()
	event = Event.query.filter_by(id=event_id).first()
	if form.validate_on_submit():
		#check which fields have been changed
		if form.new_type.data != event.type:
			event.edited_type = True
			event.type = form.new_type.data
		if form.new_date.data != event.date:
			event.edited_date = True
			event.date = form.new_date.data
		if form.new_location.data != event.location:
			event.edited_location = True
			event.location = form.new_location.data
		if form.new_time.data != event.time:
			event.edited_time = True
			event.time = form.new_time.data
		if form.new_description.data != event.description:
			event.edited_description = True
			event.description = form.new_description.data
		if form.delete.data:
			db.session.delete(event)
		db.session.commit()
		return redirect(url_for('index'))
	return render_template('editevent.html',
							form=form,
							event=event)






















