# path="/register"

from pymongo import MongoClient

import genparts

import hashlib

def get(ts, r, args, s):
	# Generate Top
	r_top = genparts.genTop("Register", s.headers)

	# Generate Bottom
	r_bottom = genparts.genBottom(ts)

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