#import environ keys
import os
# import app configuration class
from blogsite.config import Config
from flask import Flask
#import database
from flask_sqlalchemy import SQLAlchemy
#running migrations
from flask_migrate import Migrate
#creates encrypted password 
from flask_bcrypt import Bcrypt
#module for login commands
from flask_login import LoginManager
#module to send mail
from flask_mail import Mail

db = SQLAlchemy()
#Encrypted Password
bcrypt = Bcrypt()
migrate = Migrate()

#login manager customization
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message_category = 'info'
mail = Mail()

def create_app(config_class=Config):
	#set the app variable to Flask
	app = Flask(__name__)
	#Make sure config file is created with config class
	app.config.from_object(os.environ.get('APP_SETTINGS'))

	#app extensions
	#***************************
	
	db.init_app(app)
	migrate.init_app(app, db)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)
	#**************************

	# import routes after DB to prevent looping
	#***************************
	#your routes will go in here
	from blogsite.blueprints.users.routes import users
	app.register_blueprint(users)
	from blogsite.blueprints.main.routes import main
	app.register_blueprint(main)
	from blogsite.blueprints.sessions.routes import sessions
	app.register_blueprint(sessions)
	from blogsite.blueprints.passwords.routes import passwords
	app.register_blueprint(passwords)
	#**************************

	return app