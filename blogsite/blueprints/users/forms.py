# form module to be used
from flask_wtf import FlaskForm
# file uploading
from flask_wtf.file import FileField, FileAllowed
# form fields for the forms used
from wtforms import StringField, PasswordField, SubmitField, BooleanField
# validators for the forms used
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

#variables called in forms imported from other files
from blogsite.models import User
from flask_login import current_user



############# USER FORMS #####################

# USER CREATE/NEW FORM
class RegistrationForm(FlaskForm):
	#pass validations as arguments
	username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
	submit = SubmitField('Sign Up')

	#custom validation for username
	def validate_username(self, username):
		user = User.query.filter_by(username=username.data).first()

		if user:
			raise ValidationError('Username already exist. Please choose a different username.')

	#custom validation for email
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()
		if user:
			raise ValidationError('Email already exist. Please choose a different username.')

# USER UPDATE/EDIT FORM
class UpdateAccountForm(FlaskForm):
	#pass validations as arguments
	username = StringField('Username', 
		validators=[DataRequired(), Length(min=2, max=20)])
	email = StringField('Email', 
		validators=[DataRequired(), Email()])
	picture = FileField('Update Profile Picture', validators=[FileAllowed(['jpg', 'png'])])
	submit = SubmitField('Update')

	#custom validation for username
	def validate_username(self, username):
		if username.data != current_user.username:
			user = User.query.filter_by(username=username.data).first()

			if user:
				raise ValidationError('Username already exist. Please choose a different username.')

	#custom validation for email
	def validate_email(self, email):
		if email.data != current_user.email:
			user = User.query.filter_by(email=email.data).first()

			if user:
				raise ValidationError('Email already exist. Please choose a different username.')
