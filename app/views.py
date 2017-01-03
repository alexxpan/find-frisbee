from flask import render_template, flash, redirect, session, url_for, request, g, Markup
from app import app, db, lm
from .forms import LoginForm, SignupForm, NicknameForm, PasswordForm, EventForm, GoingForm, EditEventForm
from flask_login import login_user, logout_user, current_user, login_required
from .models import User, Event

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
	#sort events by time and date
	#then, make a list of forms (one for each event - sorted)
	#iterate through all the forms, checking if each one is validated on submit (only one submitted at a time)
	#if it is, add that user to the going list of the event and commit(check if this back populates and adds event to user's events)
	#in index.html, when iterating through events, display each form (by index)
	user = g.user
	events = Event.query.all()
	forms = []
	for i in range(len(events)):
		forms.append(GoingForm(prefix="form%s" % i))
	for i in range(len(forms)):
		if forms[i].validate_on_submit() and forms[i].edit_event and events[i].host_id == user.id:
			return redirect(url_for('editevent', event_id = events[i].id))
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
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('index'))
	if form.validate_on_submit():
		session['remember_me'] = form.remember_me.data
		user = User.query.filter_by(email=form.email.data).first()
		if user is None:
			message = Markup('No account associated with given email address. Please try again or sign up <a href="/signup">here</a>.')
			flash(message)
			return redirect(url_for('login'))
		if user.password != form.password.data:
			flash('Incorrect password. Please try again.')
			return redirect(url_for('login'))
		remember_me = False
		if 'remember_me' in session:
			remember_me = session['remember_me']
			session.pop('remember_me', None)
		login_user(user, remember = remember_me)
		return redirect(request.args.get('next') or url_for('index'))
	return render_template('login.html',
							form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()
	if g.user is not None and g.user.is_authenticated:
		return redirect(url_for('index'))
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user is not None:
			message = Markup('An account already exists for the given email address. Please try again or log in <a href="/login">here</a>.')
			flash(message)
			return redirect(url_for('signup'))
		user = User(nickname=form.nickname.data, email=form.email.data, password=form.password.data)
		db.session.add(user)
		db.session.commit()
		flash('Account creation success. Please log in below.')
		return redirect('/login')
	return render_template('signup.html',
							form=form)

@app.route('/logout')
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






















