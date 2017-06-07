# path="/admin"

from pymongo import MongoClient
from functions import getRank, checkLogin

import genparts

import hashlib

def get(ts, r, args, s):
	# Redirect if not an admin
	if getRank(s.headers) != 10:
		return "Redirect: /"

	# Generate Top
	sections = []
	r_top = genparts.genTop("Admin Control Panel", s.headers, sections)

	# Generate Bottom
	r_bottom = genparts.genBottom(ts)

	# Connect to Mongo DB
	client = MongoClient("mongodb://localhost:27017/")
	db = client.db
	colCategories = db.categories
	colForums = db.forums

	# Get categories
	r_forumLayout = ""

	# Loop through categories
	i = 0
	for cat in colCategories.find().sort("order", 1):
		j = 0
		r_forumLayout += "<li id=\"sortableCategory"+str(i)+"\">"+cat["title"]+"<ul id=\"sortableForums"+str(i)+"\">"

		# Loop through forums in category
		for forum in colForums.find({"cat": cat["_id"]}).sort("order", 1):
			r_forumLayout += "<li id=\"sortableForum"+str(j)+"\">"+forum["name"]+"</li>"
			j += 1

		r_forumLayout += "</ul></li>"
		i += 1

	# Return modified template
	return r.format(top=r_top,bottom=r_bottom,forumLayout=r_forumLayout)

def post(s, form, args):
	return "/admin"