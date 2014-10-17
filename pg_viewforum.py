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
	colForums = db.forums
	colThreads = db.threads

	# Load Top Template
	with open ("html/subsections/top.html", "r") as file:
		tempTop = file.read()

	# Load Bottom Template
	with open ("html/subsections/bottom.html", "r") as file:
		tempBottom = file.read()

	# Load Header Template
	with open ("html/subsections/header.html", "r") as file:
		tempHeader = file.read()

	# Load Thread Template
	with open ("html/subsections/thread.html", "r") as file:
		tempThread = file.read()

	# Get Forum Name
	forum = colForums.find_one({"_id": ObjectId(args["f"])})
	r_forumName = forum["name"]

	# Generate Top
	r_top = tempTop.format(header=tempHeader,pageTitle="View Forum | " + r_forumName)

	# Generate Page
	r_threads = ""

	for thread in colThreads.find({"forum": ObjectId(args["f"])}).sort("order", 1):
		r_threads += tempThread.format(tid=thread["_id"],title=thread["title"],author=thread["author"],replyNum=thread["numReplies"],viewNum=thread["numViews"],lastPost="")

	# Time it took to generate this page
	r_elapsed = time.time()-ts

	# Generate Bottom
	r_bottom = tempBottom.format(time=r_time,elapsed=r_elapsed)

	# Return modified template
	return r.format(threads=r_threads,top=r_top,bottom=r_bottom,forumName=r_forumName)