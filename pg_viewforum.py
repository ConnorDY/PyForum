# path="/viewforum"

from pymongo import MongoClient
from bson.objectid import ObjectId

import time
import datetime

from loadtemplates import loadTemplates
import genparts

def get(ts, r, args, s):
	# Connect to Mongo DB
	client = MongoClient("mongodb://localhost:27017/")
	db = client.db
	colForums = db.forums
	colThreads = db.threads
	colPosts = db.posts

	# Load Thread Template
	temps = loadTemplates(["thread"])

	# Get Forum Name
	forum = colForums.find_one({"_id": ObjectId(args["f"])})
	r_forumName = forum["name"]
	r_numThreads = forum["numThreads"]

	# Generate Navigation Tree
	sections = []
	sections.append(dict(text=forum["name"], link="viewforum?f={}".format(args["f"])))

	# Generate Top
	r_top = genparts.genTop("View Forum | " + r_forumName, s.headers, sections)

	# Generate Page
	r_threads = ""

	for thread in colThreads.find({"forum": ObjectId(args["f"])}).sort("bumpNum", -1):
		# Get last post in thread
		post = colPosts.find_one({"_id": thread["lastPost"]})

		# Last post time
		lastPostTime = datetime.datetime.fromtimestamp(post["time"]).strftime("%a %b %d, %Y %I:%M %p")

		# Create last post string
		r_lastPost = "<p class=\"topicdetails\" style=\"white-space: nowrap;\">{}</p>".format(lastPostTime)
		r_lastPost += "<p class=\"topicdetails\">"
		r_lastPost += "<a href=\"./member?u=\" style=\"color: #AA0000;\" class=\"username-coloured\">{}&nbsp;".format(post["author"])
		r_lastPost += "<a href=\"./viewthread?t={}\"><img src=\"./styles/acidtech/imageset/icon_topic_latest.gif\" width=\"13\" height=\"9\" alt=\"View the latest post\" title=\"View the latest post\"></a>".format(post["thread"])
		r_lastPost += "</p>"

		# Add to Thread string
		r_threads += temps["thread"].format(tid=thread["_id"],title=thread["title"],author=thread["author"],numReplies=thread["numReplies"],numViews=thread["numViews"],lastPost=r_lastPost)

	# Generate Bottom
	r_bottom = genparts.genBottom(ts)

	# Return modified template
	return r.format(threads=r_threads,top=r_top,bottom=r_bottom,forumName=r_forumName,fid=args["f"],numThreads=r_numThreads)