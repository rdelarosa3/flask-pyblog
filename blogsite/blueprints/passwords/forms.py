# form module to be used
from flask_wtf import FlaskForm
# form fields for the forms used
from wtforms import StringField, PasswordField, SubmitField, BooleanField
# validators for the forms used
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

#variables called in forms imported from other files
from blogsite.models import User
from flask_login import current_user


# USER PASSWORD RESET REQUEST FORM
class RequestResetForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	submit = SubmitField('Request Password Reset')

	#custom validation for email
	def validate_email(self, email):
		user = User.query.filter_by(email=email.data).first()

		if user is None:
			raise ValidationError('There is no account with that email. Please Register.')

# USER PASSWORD RESET/NEW FORM
class ResetPasswordForm(FlaskForm):
	password = PasswordField('Password', validators=[DataRequired()])
	confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

	submit = SubmitField('Reset Password')