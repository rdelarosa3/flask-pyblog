from sqlalchemy import event#, Table, Column, Integer, ForeignKey, UniqueConstraint, Index
from sqlalchemy.orm import validates
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
#login_manager for login def
from blogsite import db, login_manager 
from flask_login import UserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
#added to use app_create function
from flask import current_app


# REQUIRED FOR LOGIN
@login_manager.user_loader
def load_user(user_id):
    try:
        return User.query.get(user_id)
    except:
        return None

############### USER MODEL ################################################

class User(db.Model, UserMixin):
	__tablename__ = 'users'
	id = db.Column(db.Integer, primary_key=True)
	username = db.Column(db.String(20), unique=True, nullable=False)
	email = db.Column(db.String(120), unique=True, nullable=False)
	image_file = db.Column(db.String())
	password = db.Column(db.String(60), nullable=False)
	## backref allows relationship lazy will load db as necessary
	posts = db.relationship('Post', backref='user', lazy=True)

	#TOKEN CREATION-- will expire in 30 minutes for the user
	def get_reset_token(self, expires_sec=1800):
		s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
		return s.dumps({'user_id': self.id}).decode('utf-8')

	# TOKEN VERIFICATION
	#staticmethod tell python not to accept self as an argument only the given arugment 
	@staticmethod
	def verify_reset_token(token):
		s = Serializer(current_app.config['SECRET_KEY'])
		try:
			user_id = s.loads(token)['user_id']
		except:
			return None
		return User.query.get(user_id)

	def __repr__(self):
		return f"User('{self.username}', '{self.email}','{self.image_file}')"

############### POST MODEL ################################################

class Post(db.Model):
	__tablename__ = 'posts'
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
	content = db.Column(db.Text, nullable=False)
	post_image = db.Column(db.String())
	#relationship
	user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

	def __repr__(self):
		return f"Post('{self.title}', '{self.date_posted}'"
