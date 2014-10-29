from pymongo import MongoClient
from http import cookies

def checkLogin(headers):
	if headers.get("Cookie") is None:
		return False
        
	# Retrieve Cookies
	C = cookies.SimpleCookie()
	C.load(headers.get("Cookie"))
	
	# Connect to Mongo DB
	client = MongoClient("mongodb://localhost:27017/")
	db = client.db
	col = db.users

	# Check Password
	user = col.find_one({"username": C["username"].value})

	if user:
		if user["password"] == C["password"].value:
			#print("Login correct.")
			return True
		else:
			#print("Invalid password.")
			return False
	else:
		#print("User not found.")
		return False

def getUsername(headers):
	if headers.get("Cookie") is None:
		return None

	# Retrieve Cookies
	C = cookies.SimpleCookie()
	C.load(headers.get("Cookie"))
	
	# Return username
	return C["username"].value

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