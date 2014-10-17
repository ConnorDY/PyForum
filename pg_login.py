# path="/login"

from pymongo import MongoClient

import genparts
import checklogin

import hashlib

def get(ts, r, args, s):
	# Generate Top
	r_top = genparts.genTop("Login")

	# Generate Bottom
	r_bottom = genparts.genBottom(ts)

	# Return modified template
	return r.format(top=r_top,bottom=r_bottom)

def post(s, form):
	fields = ["username", "password"]
	if not all(str in form for str in fields):
		print("Form not filled out completely.")
		return

	# Connect to Mongo DB
	client = MongoClient("mongodb://localhost:27017/")
	db = client.db
	col = db.users

	# Hash inputted password
	hash_object = hashlib.sha256(bytes(form["password"].value, "utf-8"))
	password = hash_object.hexdigest()

	# Check Password
	user = col.find_one({"username": form["username"].value})

	if user:
		if user["password"] == password:
			print("Login correct.")
			s.send_header("Set-Cookie", "username={}".format(form["username"].value))
			s.send_header("Set-Cookie", "password={}".format(password))
		else:
			print("Invalid password.")
	else:
		print("User not found.")

	print("User input: {}".format(form["username"].value))

	return "/index"