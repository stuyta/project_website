from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from app import db
from flask_login import UserMixin
from app import login

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

#Defining a model space here for a list of users
class User(UserMixin, db.Model):
	#Making columns for each thing
	id = db.Column(db.Integer, primary_key = True)
	username = db.Column(db.String(64), index=True, unique=True)
	email = db.Column(db.String(120), index=True, unique=True)
	password_hash = db.Column(db.String(120)) #stores a hashed password
	posts = db.relationship('Post', backref='author', lazy='dynamic')

	def __repr__(self):
		return self.username
	#password set
	def set_password(self, password):
		self.password_hash = generate_password_hash(str(password)) #hashes the password for security
    #password recognition
	def check_password(self, password):
		return check_password_hash(self.password_hash, str(password))
#Defining a post that is mapped to each user
class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(100), index=True, unique=True)
	body = db.Column(db.String(5300), index=True, unique=True)
	timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
	user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
	
	#returns what the post actually says
	def __repr__(self):
		return self.body
