import os
import secrets
#added current_app to use app_create function
from flask import url_for, current_app
# send email messages
from flask_mail import Message
# imports required variables from __init__
from blogsite import mail

########### PASSWORD RESET ROUTES ######################

def send_reset_email(user):
	token = user.get_reset_token()
	msg = Message('Password Reset Request', sender='noreply@demo.com', recipients=[user.email])
	msg.body = f''' To reset your password, visit the following link: {url_for('passwords.reset_token',token=token, _external=True)}

	If you did not make this request then simply ignore this email no change has been made.
	'''
	mail.send(msg)