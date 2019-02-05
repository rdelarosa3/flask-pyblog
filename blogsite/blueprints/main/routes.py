from flask import render_template, request, Blueprint
import os
#imports the models
# from blogsite.models import Post

main = Blueprint('main', __name__)

# APP INDEX/HOMEPAGE
@main.route("/")
#set multiple routes to same page
@main.route("/homepage")
def home():
	# return the template for route page
	return render_template('home.html')
