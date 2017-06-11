# path="/login"

from pymongo import MongoClient
from functions import checkLogin

import global_vars
import genparts

import hashlib

def get(ts, r, args, s):
	# Redirect if already logged in
	if checkLogin(s.headers):
		return "Redirect: /"

	# Generate Top
	sections = []
	r_top = genparts.genTop("Login", s.headers, sections)

	# Generate Bottom
	r_bottom = genparts.genBottom(ts)

	# Return modified template
	return r.format(top=r_top,bottom=r_bottom)

def post(s, form, args):
	# Make sure values entered are alright
	from functions import checkFieldsBlank
	fields = ["username", "password"]
	if checkFieldsBlank(form, fields):
		return "/login"

	# Connect to Mongo DB
	client = MongoClient(MONGODB)
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
			return "/"
		else:
			print("Invalid password.")
			return "/login"
	else:
		print("User not found.")
		return "/login"