from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5


class User(UserMixin,db.Model):
	id=db.Column(db.Integer,primary_key=True)
	username= db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	#donations_made=db.relationship('Donations',backref='donor',lazy='dynamic')	

	def set_password(self,password):
		self.password_hash=generate_password_hash(password)
	
	def check_password(self,password):
		return check_password_hash(self.password_hash,password)

	def __repr__(self):
		return '<User {}>'.format(self.username)

class NGO(UserMixin,db.Model):
	id=db.Column(db.Integer,primary_key=True)
	orgname=db.Column(db.String(64),index=True,unique=True)
	email=db.Column(db.String(120),index=True,unique=True)
	password_hash=db.Column(db.String(128))
	field_of_work=db.Column(db.String(100))
	about=db.Column(db.String(207))
	donations_recieved=db.relationship('Donations',backref='donated_to',lazy='dynamic')
	members=db.relationship('Volunteer',backref='members',lazy='dynamic')

	def set_password(self,password):
		self.password_hash=generate_password_hash(password)

	def check_password(self,password):
		return check_password_hash(self.password_hash,password)

	def avatar(self, size):
		digest = md5(self.email.lower().encode('utf-8')).hexdigest()
		return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

	def __repr__(self):
		return '<NGO {}>'.format(self.orgname)



class Volunteer(UserMixin,db.Model):
	id=db.Column(db.Integer,primary_key=True)
	uname = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(128))
	about=db.Column(db.String(207))
	related_with=db.Column(db.String(64),db.ForeignKey(NGO.orgname))

	def set_password(self,password):
		self.password_hash=generate_password_hash(password)
	
	def check_password(self,password):
		return check_password_hash(self.password_hash,password)
	def avatar(self, size):
		digest = md5(self.email.lower().encode('utf-8')).hexdigest()
		return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)

	def __repr__(self):
		return '<Volunteer {}>'.format(self.uname)


class Donations(db.Model):
	id=db.Column(db.Integer,primary_key=True)
	username=db.Column(db.String(64),db.ForeignKey(User.username))
	orgname=db.Column(db.String(64),db.ForeignKey(NGO.orgname))
	#campaign=db.Column(db.String(100))
	amount=db.Column(db.Integer)

	def __repr__(self):
		return '<Donation {}>'.format(self.id)

@login.user_loader
def load_user(id):
    return User.query.get(int(id))
@login.user_loader
def load_volunteer(id):
    return Volunteer.query.get(int(id))
@login.user_loader
def load_ngo(id):
	return NGO.query.get(int(id))
"""
def init_db():
    db.create_all()

if __name__ == '__main__':
    init_db()
"""

