from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint)
#imports required variables for logged in session
from flask_login import login_user, current_user, logout_user, login_required
#imports the models
from blogsite.models import User
#import each created form classes from forms.py
from blogsite.blueprints.sessions.forms import LoginForm
# imports required variables from __init__
from blogsite import db, bcrypt


sessions = Blueprint('sessions', __name__)

############# SESSION RESOURCES/ROUTES #####################

# SESSION NEW/CREATE
@sessions.route("/login", methods=['GET', 'POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	#set form = imported LoginForm Class
	form = LoginForm()
	if form.validate_on_submit():
		# find user and see of email match password
		user = User.query.filter_by(email=form.email.data).first()
		if user and bcrypt.check_password_hash(user.password, form.password.data):
			#login user if all information matches
			login_user(user, remember=form.remember.data)
			flash(f'Welcome back {user.username}!', 'success')
			# if coming from a required login page redirect to that page
			next_page = request.args.get('next')
			return redirect(next_page) if next_page else redirect(url_for('main.home'))
		else:
			flash('Login unsuccessful. Please check email and password', 'danger')
	return render_template('login.html', title='Login', form=form)#call form as argument

# SESSION DELETE
@sessions.route("/logout")
def logout():
	logout_user()
	return redirect(url_for('main.home'))