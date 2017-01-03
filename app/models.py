from app import db

association_table = db.Table('association', db.Model.metadata,
		db.Column('user_id', db.Integer, db.ForeignKey('user.id')),
		db.Column('event_id', db.Integer, db.ForeignKey('event.id'))
		)

class User(db.Model):
	__tablename__ = 'user'
	id = db.Column(db.Integer, primary_key=True)
	nickname = db.Column(db.String(64), index=True, unique=False)
	email = db.Column(db.String(120), index=True, unique=True)
	password = db.Column(db.String(120), index=True, unique=False)
	events = db.relationship("Event", secondary=association_table, back_populates="going")

	@property
	def is_authenticated(self):
		return True

	@property
	def is_active(self):
		return True

	@property
	def is_anonymous(self):
		return False

	def get_id(self):
		try:
			return unicode(self.id)
		except NameError:
			return str(self.id)

	def __repr__(self):
		return '<User %r>' % (self.nickname)

class Event(db.Model):
	__tablename__ = 'event'
	id = db.Column(db.Integer, primary_key=True)
	type = db.Column(db.String(20))
	date = db.Column(db.String(20))
	location = db.Column(db.String(50))
	time = db.Column(db.String(20))
	description = db.Column(db.String(140))
	host_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	edited_type = db.Column(db.Boolean, default=False)
	edited_date = db.Column(db.Boolean, default=False)
	edited_location = db.Column(db.Boolean, default=False)
	edited_time = db.Column(db.Boolean, default=False)
	edited_description = db.Column(db.Boolean, default=False)
	going = db.relationship("User", secondary=association_table, back_populates="events")

	def __repr__(self):
		return '<Type %r>' % (self.type)




