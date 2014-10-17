# path="/register"

from pymongo import MongoClient

from loadtemplates import loadTemplates

import time
import datetime
import hashlib

def get(ts, r, args, s):
	# Current date and time
	r_time = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S %m/%d/%Y")

	# Connect to Mongo DB
	client = MongoClient("mongodb://localhost:27017/")
	db = client.db
	colCategories = db.categories
	colForums = db.forums

	# Load Top Template
	temps = loadTemplates(["top", "bottom", "header"])

	# Generate Top
	r_top = temps["top"].format(header=temps["header"],pageTitle="Register")

	# Time it took to generate this page
	r_elapsed = time.time()-ts

	# Generate Bottom
	r_bottom = temps["bottom"].format(time=r_time,elapsed=r_elapsed)

	# Return modified template
	return r.format(top=r_top,bottom=r_bottom)

def post(s, form):
	# Make sure values entered are alright
	#form = {key: value.strip() for key, value in form.items() if value.strip()}
	fields = ["username", "email", "password"]
	if not all(str in form for str in fields):
		print("Form not filled out completely.")
		return

	# Connect to Mongo DB
	client = MongoClient("mongodb://localhost:27017/")
	db = client.db
	col = db.users

	# Insert user into database
	hash_object = hashlib.sha256(bytes(form["password"].value, "utf-8"))
	password = hash_object.hexdigest()

	user = {"username": form["username"].value,
			"email": form["email"].value,
			"password": password}
	col.insert(user)

	print("New user created: {}".format(form["username"].value))

	return "/index"