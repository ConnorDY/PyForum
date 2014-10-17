# path="/index"

from pymongo import MongoClient

import http.server

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
	with open ("html/subsections/top.html", "r") as file:
		tempTop = file.read()

	# Load Bottom Template
	with open ("html/subsections/bottom.html", "r") as file:
		tempBottom = file.read()

	# Load Header Template
	with open ("html/subsections/header.html", "r") as file:
		tempHeader = file.read()

	# Load Forum Template
	with open ("html/subsections/forum.html", "r") as file:
		tempForums = file.read()

	# Load Category Template
	with open ("html/subsections/category.html", "r") as file:
		tempCategories = file.read()

	# Generate Top
	r_top = tempTop.format(header=tempHeader,pageTitle="Forums")

	## Create Page ##
	r_board = ""

	# Loop through categories
	for cat in colCategories.find().sort("order", 1):
		r_forums = ""

		# Loop through forums in category
		for forum in colForums.find({"cat": cat["_id"]}).sort("order", 1):
			r_forums += tempForums.format(fid=forum["_id"],forumName=forum["name"],forumDesc=forum["desc"],topicNum=forum["numTopics"],postNum=forum["numPosts"],lastPostTime="")
		
		r_categories = tempCategories.format(cid=cat["_id"],title=cat["title"],forums=r_forums)
		r_board += r_categories+"<br />"

	# Time it took to generate this page
	r_elapsed = time.time()-ts

	# Generate Bottom
	r_bottom = tempBottom.format(time=r_time,elapsed=r_elapsed)

	# Return modified template
	return r.format(board=r_board,top=r_top,bottom=r_bottom)