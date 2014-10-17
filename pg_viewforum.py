# path="/viewforum"

from pymongo import MongoClient
from bson.objectid import ObjectId

from loadtemplates import loadTemplates

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
	temps = loadTemplates(["top", "bottom", "header", "thread"])

	# Get Forum Name
	forum = colForums.find_one({"_id": ObjectId(args["f"])})
	r_forumName = forum["name"]

	# Generate Top
	r_top = temps["top"].format(header=temps["header"],pageTitle="View Forum | " + r_forumName)

	# Generate Page
	r_threads = ""

	for thread in colThreads.find({"forum": ObjectId(args["f"])}).sort("order", 1):
		r_threads += temps["thread"].format(tid=thread["_id"],title=thread["title"],author=thread["author"],replyNum=thread["numReplies"],viewNum=thread["numViews"],lastPost="")

	# Time it took to generate this page
	r_elapsed = time.time()-ts

	# Generate Bottom
	r_bottom = temps["bottom"].format(time=r_time,elapsed=r_elapsed)

	# Return modified template
	return r.format(threads=r_threads,top=r_top,bottom=r_bottom,forumName=r_forumName)