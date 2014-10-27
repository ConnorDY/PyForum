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
