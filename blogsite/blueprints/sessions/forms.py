# form module to be used
from flask_wtf import FlaskForm
# form fields for the forms used
from wtforms import StringField, PasswordField, SubmitField, BooleanField
# validators for the forms used
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError

############# SESSION FORM #####################

# SESSION CREATE/NEW FORM 
class LoginForm(FlaskForm):
	#pass validations as arguments
	email = StringField('Email', 
		validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')