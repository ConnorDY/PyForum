# path="/index"

from pymongo import MongoClient
import http.server

import time
import datetime

from loadtemplates import loadTemplates
import genparts

def get(ts, r, args, s):
	# Connect to Mongo DB
	client = MongoClient("mongodb://localhost:27017/")
	db = client.db
	colCategories = db.categories
	colForums = db.forums
	colPosts = db.posts

	# Load Templates
	temps = loadTemplates(["forum", "category"])

	# Generate Top
	sections = []
	r_top = genparts.genTop("Forums", s.headers, sections)

	## Create Page ##
	r_board = ""

	# Loop through categories
	for cat in colCategories.find().sort("order", 1):
		r_forums = ""

		# Loop through forums in category
		for forum in colForums.find({"cat": cat["_id"]}).sort("order", 1):
			r_lastPost = "No posts"

			if "lastPost" in forum:
				# Get last post in forum
				post = colPosts.find_one({"_id": forum["lastPost"]})
				
				# Last post time
				lastPostTime = datetime.datetime.fromtimestamp(post["time"]).strftime("%a %b %d, %Y %I:%M %p")

				# Create last post string
				r_lastPost = "<p class=\"topicdetails\" style=\"white-space: nowrap;\">{}</p>".format(lastPostTime)
				r_lastPost += "<p class=\"topicdetails\">"
				r_lastPost += "<a href=\"./member?u=\" style=\"color: #AA0000;\" class=\"username-coloured\">{}&nbsp;".format(post["author"])
				r_lastPost += "<a href=\"./viewthread?t={}\"><img src=\"./styles/acidtech/imageset/icon_topic_latest.gif\" width=\"13\" height=\"9\" alt=\"View the latest post\" title=\"View the latest post\"></a>".format(post["thread"])
				r_lastPost += "</p>"

			# Add to Forum string
			r_forums += temps["forum"].format(fid=forum["_id"],forumName=forum["name"],forumDesc=forum["desc"],numThreads=forum["numThreads"],numPosts=forum["numPosts"],lastPost=r_lastPost)
		
		# Add to Board string
		r_categories = temps["category"].format(cid=cat["_id"],title=cat["title"],forums=r_forums)
		r_board += r_categories+"<br />"

	# Generate Bottom
	r_bottom = genparts.genBottom(ts)

	# Return modified template
	return r.format(board=r_board,top=r_top,bottom=r_bottom)