# path="/viewforum"

from pymongo import MongoClient
from bson.objectid import ObjectId

import time
import datetime

def get(ts, r, args, s):
	# Current date and time
	r_time = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S %m/%d/%Y")

	# Connect to Mongo DB
	client = MongoClient("mongodb://localhost:27017/")
	db = client.db
	#colCategories = db.categories
	#colForums = db.forums
	colThreads = db.threads
	colPosts = db.posts

	# Load Top Template
	with open ("html/subsections/top.html", "r") as file:
		tempTop = file.read()

	# Load Bottom Template
	with open ("html/subsections/bottom.html", "r") as file:
		tempBottom = file.read()

	# Load Header Template
	with open ("html/subsections/header.html", "r") as file:
		tempHeader = file.read()

	# Load Post Template
	with open ("html/subsections/post.html", "r") as file:
		tempPost = file.read()

	# Get Thread Info
	thread = colThreads.find_one({"_id": ObjectId(args["t"])})
	r_threadName = thread["title"]
	r_tid = thread["_id"]

	# Generate Top
	r_top = tempTop.format(header=tempHeader,pageTitle="View Thread | " + r_threadName)

	# Generate Page
	r_posts = ""

	for post in colPosts.find({"thread": ObjectId(args["t"])}).sort("_id", 1):
		r_posts += tempPost.format(author=post["author"],content=post["content"],postTime="")

	# Time it took to generate this page
	r_elapsed = time.time()-ts

	# Generate Bottom
	r_bottom = tempBottom.format(time=r_time,elapsed=r_elapsed)

	# Return modified template
	return r.format(posts=r_posts,top=r_top,bottom=r_bottom,threadName=r_threadName,tid=r_tid)