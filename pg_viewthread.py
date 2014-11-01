# path="/viewthread"

from pymongo import MongoClient
from bson.objectid import ObjectId

import time
import datetime

from loadtemplates import loadTemplates
import genparts

from functions import getUsernameById
from functions import formatPost
from functions import formatPostDB

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

	forum = colForums.find_one({"_id": thread["forum"]})

	# Generate Navigation Tree
	navSections = []
	navSections.append(dict(text=forum["name"], link="viewforum?f={}".format(forum["_id"])))
	navSections.append(dict(text=thread["title"], link="viewthread?t={}".format(args["t"])))

	# Generate Top
	r_top = genparts.genTop("View Thread | " + r_threadName, s.headers, navSections)

	# Generate Page
	r_posts = ""

	for post in colPosts.find({"thread": ObjectId(args["t"])}).sort("_id", 1):
		r_postTime = datetime.datetime.fromtimestamp(post["time"]).strftime("%a %b %d, %Y %I:%M %p")

		r_posts += temps["post"].format(author=getUsernameById(post["author"]),content=formatPostDB(post["content"]),postTime=r_postTime)

	# Update thread views
	colThreads.update({"_id": ObjectId(args["t"])}, {"$inc": {"numViews": 1}}, upsert=False, multi=False)

	# Generate Bottom
	r_bottom = genparts.genBottom(ts)

	# Return modified template
	return r.format(posts=r_posts,top=r_top,bottom=r_bottom,threadName=r_threadName,tid=r_tid)

	
def post(s, form, args):
	page = "/viewthread?t={}".format(args["t"])

	from functions import checkLogin

	# Redirect if not logged in
	if not checkLogin(s.headers):
		return "/login"

	# Import needed functions
	from functions import getUsername
	from functions import getUserId
	from functions import checkFieldsBlank

	# Make sure values entered are alright
	fields = ["message"]
	if checkFieldsBlank(form, fields):
		return page

	# Connect to Mongo DB
	client = MongoClient("mongodb://localhost:27017/")
	db = client.db

	# Get Collections
	colForums = db.forums
	colThreads = db.threads
	colPosts = db.posts

	# Insert reply into database
	reply = {"thread": ObjectId(args["t"]),
			"author": getUserId(getUsername(s.headers)),
			"content": formatPost(form["message"].value),
			"time": time.time()}
	
	post_id = colPosts.insert(reply)

	# Update replies and posts counts
	thread = colThreads.find_one({"_id": ObjectId(args["t"])})
	colThreads.update({"_id": ObjectId(args["t"])}, {"$inc": {"numReplies": 1}}, upsert=False, multi=False)
	colForums.update({"_id": thread["forum"]}, {"$inc": {"numPosts": 1}}, upsert=False, multi=False)

	# Get and increase bump number for forum, update bump number for thread
	colForums.update({"_id": thread["forum"]}, {"$inc": {"bump": 1}}, upsert=False, multi=False)
	forum = colForums.find_one({"_id": thread["forum"]})
	colThreads.update({"_id": ObjectId(args["t"])}, {"$set": {"bumpNum": forum["bump"]}}, upsert=False, multi=False)

	# Update last posts in forum and thread
	colForums.update({"_id": thread["forum"]}, {"$set": {"lastPost": post_id}}, upsert=False, multi=False)
	colThreads.update({"_id": ObjectId(args["t"])}, {"$set": {"lastPost": post_id}}, upsert=False, multi=False)

	return page