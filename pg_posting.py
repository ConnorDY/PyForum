# path="/posting"

from pymongo import MongoClient
from bson.objectid import ObjectId

from loadtemplates import loadTemplates
import genparts

from functions import formatPost

def get(ts, r, args, s):
	# Connect to Mongo DB
	client = MongoClient(MONGODB)
	db = client.db
	colForums = db.forums
	colThreads = db.threads

	# Get Forum Name
	forum = colForums.find_one({"_id": ObjectId(args["f"])})
	r_forumName = forum["name"]

	# Generate Navigation Tree
	sections = []
	sections.append(dict(text=forum["name"], link="viewforum?f={}".format(args["f"])))

	# Generate Top
	r_top = genparts.genTop("Creating a Thread | " + r_forumName, s.headers, sections)

	# Generate Bottom
	r_bottom = genparts.genBottom(ts)

	# Return modified template
	return r.format(top=r_top,bottom=r_bottom,forumName=r_forumName,fid=args["f"])

def post(s, form, args):
	page = "/posting?f={}".format(args["f"])

	# Make sure values entered are alright
	from functions import checkFieldsBlank
	fields = ["subject", "message"]
	if checkFieldsBlank(form, fields):
		return page

	# Import needed functions
	from functions import checkLogin
	import time
	import datetime

	# Redirect if not logged in
	if not checkLogin(s.headers):
		return "/login"

	from functions import getUsername
	from functions import getUserId

	# Connect to Mongo DB
	client = MongoClient(MONGODB)
	db = client.db

	# Get Collections
	colForums = db.forums
	colThreads = db.threads
	colPosts = db.posts

	# Get username
	username = getUsername(s.headers)
	userId = getUserId(username)

	# Get and increase bump number for forum
	colForums.update({"_id": ObjectId(args["f"])}, {"$inc": {"bump": 1}}, upsert=False, multi=False)
	forum = colForums.find_one({"_id": ObjectId(args["f"])})
	bump = forum["bump"]

	# Insert thread into database
	thread = {"forum": ObjectId(args["f"]),
			  "title": form["subject"].value,
			  "author": userId,
			  "numReplies": 0,
			  "numViews": 0,
			  "bumpNum": bump}

	thread_id = colThreads.insert(thread)

	# Insert first post into database
	post = {"thread": thread_id,
			"author": userId,
			"content": formatPost(form["message"].value),
			"time": time.time()}

	post_id = colPosts.insert(post)

	# Update threads and posts counts
	colForums.update({"_id": ObjectId(args["f"])}, {"$inc": {"numPosts": 1}}, upsert=False, multi=False)
	colForums.update({"_id": ObjectId(args["f"])}, {"$inc": {"numThreads": 1}}, upsert=False, multi=False)

	# Update last posts in forum and thread
	colForums.update({"_id": ObjectId(args["f"])}, {"$set": {"lastPost": post_id}}, upsert=False, multi=False)
	colThreads.update({"_id": thread_id}, {"$set": {"lastPost": post_id}}, upsert=False, multi=False)

	return "/viewthread?t={}".format(thread_id)