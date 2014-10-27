# path="/viewthread"

from pymongo import MongoClient
from bson.objectid import ObjectId

from loadtemplates import loadTemplates
import genparts

def get(ts, r, args, s):
	# Connect to Mongo DB
	client = MongoClient("mongodb://localhost:27017/")
	db = client.db

	# Get Collections
	colCategories = db.categories
	colForums = db.forums
	colThreads = db.threads
	colPosts = db.posts

	# Load Templates
	temps = loadTemplates(["post"])

	# Get Thread Info
	thread = colThreads.find_one({"_id": ObjectId(args["t"])})
	r_threadName = thread["title"]
	r_tid = thread["_id"]

	# Generate Top
	r_top = genparts.genTop("View Thread | " + r_threadName, s.headers)

	# Generate Page
	r_posts = ""

	for post in colPosts.find({"thread": ObjectId(args["t"])}).sort("_id", 1):
		r_posts += temps["post"].format(author=post["author"],content=post["content"],postTime="")

	# Generate Bottom
	r_bottom = genparts.genBottom(ts)

	# Return modified template
	return r.format(posts=r_posts,top=r_top,bottom=r_bottom,threadName=r_threadName,tid=r_tid)

def post(s, form, args):
	page = "/viewthread?t={}".format(args["t"])

	from functions import checkLogin

	# Redirect if not logged in
	if not checkLogin(s.headers):
		return page

	# Import function to get the username from the cookie
	from functions import getUsername

	# Make sure values entered are alright
	fields = ["message"]
	if not all(str in form for str in fields):
		print("Form not filled out completely.")
		return page

	# Connect to Mongo DB
	client = MongoClient("mongodb://localhost:27017/")
	db = client.db

	# Get Collections
	colPosts = db.posts

	# Insert reply into database
	reply = {"thread": ObjectId(args["t"]),
			"author": getUsername(s.headers),
			"content": form["message"].value}
	
	colPosts.insert(reply)

	return page