from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint)
#imports required variables for logged in session
from flask_login import login_user, current_user, logout_user, login_required
#imports the models
from blogsite.models import User
#import each created form classes from forms.py
from blogsite.blueprints.passwords.forms import (ResetPasswordForm, RequestResetForm)
# imports required variables from __init__
from blogsite import db, bcrypt
# import helpers/utils
from blogsite.blueprints.passwords.utils import send_reset_email

passwords = Blueprint('passwords', __name__)

########### PASSWORD RESET ROUTES ######################

@passwords.route("/reset_password", methods=['GET','POST'])
def reset_request():
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	form = RequestResetForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		send_reset_email(user)
		flash('Instructions have been sent to your email. Please follow to reset password.','success')
		return redirect(url_for('sessions.login'))
	return render_template('reset_request.html', title='Reset Password', form=form)


@passwords.route("/reset_password/<token>", methods=['GET','POST'])
def reset_token(token):
	if current_user.is_authenticated:
		return redirect(url_for('main.home'))
	user = User.verify_reset_token(token)
	if not user:
		flash('That is an invalid or expired token', 'warning')
		return redirect(url_for('passwords.reset_request'))
	form = ResetPasswordForm()
	if form.validate_on_submit():
		# created crypted password for user on database
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user.password = hashed_password
		db.session.commit()
		flash(f'Password has been updated! You are no able to login!', 'success')
		return redirect(url_for('sessions.login'))
	return render_template('reset_token.html', title='Reset Password', form=form)