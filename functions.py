from pymongo import MongoClient
from bson.objectid import ObjectId
from html.parser import HTMLParser
from http import cookies
from types import *

def checkLogin(headers):
	if headers.get("Cookie") is None:
		return False
        
	# Retrieve Cookies
	C = cookies.SimpleCookie()
	C.load(headers.get("Cookie"))

	fields = ["username", "password"]
	if not all(str in C for str in fields):
		return False
	
	# Connect to Mongo DB
	client = MongoClient("mongodb://localhost:27017/")
	db = client.db
	col = db.users

	# Check Password
	user = col.find_one({"username": C["username"].value})

	if user is not None:
		if user["password"] == C["password"].value:
			return True # Correct
		else:
			return False # Incorrect
	else:
		return False # User not found

def getUsername(headers):
	if headers.get("Cookie") is None:
		return None

	# Retrieve Cookies
	C = cookies.SimpleCookie()
	C.load(headers.get("Cookie"))
	
	# Return username
	return C["username"].value

def getUsernameById(id_):
	# Fix type if needed
	if type(id_) != type(ObjectId("545531052c7c7c16b8946fdb")):
		id_ = ObjectId(id_)

	# Connect to Mongo DB
	client = MongoClient("mongodb://localhost:27017/")
	db = client.db
	col = db.users

	# Get user
	user = col.find_one({"_id": id_})

	# Return username
	if user is None:
		return "DNE"

	return user["username"]

def getUserId(username):
	if username is None:
		return None

	# Connect to Mongo DB
	client = MongoClient("mongodb://localhost:27017/")
	db = client.db
	col = db.users

	# Get User ID
	user = col.find_one({"username": username})

	if user is None:
		return None

	return user["_id"]

def checkFieldsBlank(form, fields):
	if not all(str in form for str in fields):
		print("Form not filled out completely.")
		return True
	else:
		for field in fields:
			if form[field].value.strip() == "":
				print("Form not filled out completely.")
				return True

	return False

class MLStripper(HTMLParser):
	def __init__(self):
		self.reset()
		self.strict = False
		self.convert_charrefs= True
		self.fed = []
	def handle_data(self, d):
		self.fed.append(d)
	def get_data(self):
		return ''.join(self.fed)

def strip_tags(html):
	s = MLStripper()
	s.feed(html)
	return s.get_data()

def addSlashes(s):
	l = ["\\", '"', "'", "\0"]

	for i in l:
		if i in s:
			s = s.replace(i, '\\'+i)

	return s

def formatPost(s):
	s = addSlashes(s)
	s = s.replace("Ã¯Â¿Â½", "\\\"")
	s = s.replace("�", "\\\"")

	return s

def formatPostDB(s):
	s = s.replace("\n", "<br />")
	s = bytes(s, "utf-8").decode("unicode_escape")
	s = s.replace("Ã¯Â¿Â½", "\"")
	s = s.replace("�", "\"")

	return s