# render_tempalte adds templates to file # url_for links to routes  
# flash and redirect are for redirection after form submital and flash message
# abort renders 403 page
from flask import (render_template, url_for, flash, redirect, request, abort, Blueprint)
#imports the models
from blogsite.models import User
#import each created form classes from forms.py
from blogsite.blueprints.users.forms import RegistrationForm, UpdateAccountForm
# imports required variables from __init__
from blogsite import db, bcrypt
#imports required variables for logged in session
from flask_login import login_user, current_user, logout_user, login_required
#image uploader
from blogsite.blueprints.users.image_helper import upload_file_to_s3, allowed_profile_images, delete_file_from_s3
#secure naming
from werkzeug.utils import secure_filename


users = Blueprint('users', __name__)
############# USER RESOURCES/ROUTES #####################

# USER CREATE/NEW
@users.route("/register", methods=['GET', 'POST'])
def register():
	#set form = imported RegistrationForm Class
	form = RegistrationForm()
	#form validation for form 
	if form.validate_on_submit():
		# created crypted password for user on database
		hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		#create user in database
		user = User(username=form.username.data, email=form.email.data, password=hashed_password)
		db.session.add(user)
		db.session.commit()
		flash(f'Account created! You are no able to login!', 'success')
		return redirect(url_for('main.home'))
	return render_template('users/new.html', title='Register', form=form)#call form as argument

# USER EDIT/UPDATE/ACCOUNT
@users.route("/users/<string:username>/edit", methods=['GET','POST'])
@login_required
def edit(username):
	user = User.query.filter_by(username=username).first_or_404()
	if user != current_user:
		abort(403)
	form = UpdateAccountForm()
	if form.validate_on_submit():
		# if form.picture.data:
		# 	file = form.picture.data
		# if file and allowed_profile_images(file.filename):
		# 	old_filename = user.image_file
		# 	delete_file_from_s3(old_filename)
		# 	file.filename = secure_filename(user.username + "-" + file.filename)
		# 	output = upload_file_to_s3(file)
		# 	current_user.picture_file = file.filename

		current_user.username = form.username.data
		current_user.email = form.email.data
		db.session.commit()
		flash('Account Updated', 'success')
		return redirect(url_for('main.home'))
	elif request.method == 'GET':
		form.username.data = current_user.username
		form.email.data = current_user.email
	# image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
	return render_template('users/edit.html', title='Account', user=current_user,form=form)

# USER PROFILE IMAGE ROUTE
@users.route("/users/<string:username>/image", methods=['POST'])
@login_required
def upload_profile_image(username):
	form = UpdateAccountForm()
	user = User.query.filter_by(username=username).first_or_404()

    # Prevent unauthorized user from changing data of another user
	if not user.id == current_user.id:
		return render_template('users/edit.html', validation_errors=['Unauthorized!'], form=form, user=user)
	# Check if image in file for upload
	if "image_file" not in request.files:
		flash("No profile image")
		return render_template('users/edit.html', validation_errors=[], form=form, user=user)

	file = request.files["image_file"]

	# if no filename ask for new image
	if file.filename == "":
		flash("Please select a file")
		return render_template('edit.html', form=form)

	# check if file extension is acceptable
	if file and allowed_profile_images(file.filename):
		# if there is a previous file delete the file
		old_filename = user.image_file
		delete_file_from_s3(old_filename)

		# create a custom name for file
		file.filename = secure_filename(user.username + "-" + file.filename)
		# upload the file
		output = upload_file_to_s3(file)
		# set the user image file equal the bucket url
		user.image_file = output
	
		db.session.commit()
		flash("Profile Picture Updated!")

		#redirect the user create the post action
		return redirect(url_for('main.home'))

	else:
		return redirect("/")





