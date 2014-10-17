# path="/index"

from pymongo import MongoClient
import http.server

from loadtemplates import loadTemplates

import time
import datetime

def get(ts, r, args, s):
	# Current date and time
	r_time = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S %m/%d/%Y")

	# Connect to Mongo DB
	client = MongoClient("mongodb://localhost:27017/")
	db = client.db
	colCategories = db.categories
	colForums = db.forums

	# Load Top Template
	temps = loadTemplates(["top", "bottom", "header", "forum", "category"])

	# Generate Top
	r_top = temps["top"].format(header=temps["header"],pageTitle="Forums")

	## Create Page ##
	r_board = ""

	# Loop through categories
	for cat in colCategories.find().sort("order", 1):
		r_forums = ""

		# Loop through forums in category
		for forum in colForums.find({"cat": cat["_id"]}).sort("order", 1):
			r_forums += temps["forum"].format(fid=forum["_id"],forumName=forum["name"],forumDesc=forum["desc"],topicNum=forum["numTopics"],postNum=forum["numPosts"],lastPostTime="")
		
		r_categories = temps["category"].format(cid=cat["_id"],title=cat["title"],forums=r_forums)
		r_board += r_categories+"<br />"

	# Time it took to generate this page
	r_elapsed = time.time()-ts

	# Generate Bottom
	r_bottom = temps["bottom"].format(time=r_time,elapsed=r_elapsed)

	# Return modified template
	return r.format(board=r_board,top=r_top,bottom=r_bottom)