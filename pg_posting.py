# path="/posting"

from pymongo import MongoClient
from bson.objectid import ObjectId

from loadtemplates import loadTemplates
import genparts

def get(ts, r, args, s):
	# Connect to Mongo DB
	client = MongoClient("mongodb://localhost:27017/")
	db = client.db
	colForums = db.forums
	colThreads = db.threads

	# Get Forum Name
	forum = colForums.find_one({"_id": ObjectId(args["f"])})
	r_forumName = forum["name"]

	# Generate Top
	r_top = genparts.genTop("Creating a Thread | " + r_forumName, s.headers)

	# Generate Navigation Tree
	sections = []
	sections.append(dict(text=forum["name"], link="viewforum?f={}".format(args["f"])))
	r_navTree = genparts.genNavTree(sections)

	# Generate Bottom
	r_bottom = genparts.genBottom(ts)

	# Return modified template
	return r.format(top=r_top,navTree=r_navTree,bottom=r_bottom,forumName=r_forumName,fid=args["f"])

def post(s, form, args):
	from functions import checkLogin

	# Redirect if not logged in
	if not checkLogin(s.headers):
		return "/login"

	from functions import getUsername

	# Connect to Mongo DB
	client = MongoClient("mongodb://localhost:27017/")
	db = client.db

	# Get Collections
	colForums = db.forums
	colThreads = db.threads
	colPosts = db.posts

	# Get username
	username = getUsername(s.headers)

	# Insert thread into database
	thread = {"forum": ObjectId(args["f"]),
			  "title": form["subject"].value,
			  "author": username,
			  "numReplies": 0,
			  "numViews": 0}

	thread_id = colThreads.insert(thread)

	# Insert first post into database
	post = {"thread": thread_id,
			"author": username,
			"content": form["message"].value}

	colPosts.insert(post)

	# Update threads and posts counts
	colForums.update({"_id": ObjectId(args["f"])}, {"$inc": {"numPosts": 1}}, upsert=False, multi=False)
	colForums.update({"_id": ObjectId(args["f"])}, {"$inc": {"numThreads": 1}}, upsert=False, multi=False)

	return "/viewthread?t={}".format(thread_id)