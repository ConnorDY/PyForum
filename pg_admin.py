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

	# Loop through categories
	r_forumLayout = ""
	r_categoriesOptions = ""
	i = 0
	j = 0
	
	for cat in colCategories.find().sort("order", 1):
		r_forumLayout += "<li id=\"sortableCategory"+str(i)+"\">"+cat["title"]+"<ul id=\"sortableForums"+str(i)+"\">"
		r_categoriesOptions += "<option value=\""+str(cat["_id"])+"\">"+cat["title"]+"</option>\n"

		# Loop through forums in category
		for forum in colForums.find({"cat": cat["_id"]}).sort("order", 1):
			r_forumLayout += "<li id=\"sortableForum"+str(j)+"\">"+forum["name"]+"</li>\n"
			j += 1

		r_forumLayout += "</ul></li>\n"
		i += 1

	# Return modified template
	return r.format(top=r_top,bottom=r_bottom,forumLayout=r_forumLayout,categoriesOptions=r_categoriesOptions)

def post(s, form, args):
	# Redirect if not an admin
	if getRank(s.headers) != 10:
		return "/"

	# Make sure values entered are alright
	from functions import checkFieldsBlank
	fields = ["ordering"]
	if checkFieldsBlank(form, fields):
		return "/admin"

	# Parse ordering
	newOrdering = form["ordering"].value.split(";")
	del newOrdering[len(newOrdering) - 1] # remove empty element
	for i in range(0, len(newOrdering)):
		newOrdering[i] = newOrdering[i][8:]

	print("Setting new ordering of categories and forums:\n   " + (", ".join(str(i) for i in newOrdering)))

	# Connect to Mongo DB
	client = MongoClient("mongodb://localhost:27017/")
	db = client.db
	colCategories = db.categories
	colForums = db.forums

	# Get current order
	catOrder = []
	forumsOrder = []

	for cat in colCategories.find().sort("order", 1):
		catOrder.append(cat["_id"])
		for forum in colForums.find({"cat":cat["_id"]}).sort("order", 1):
			forumsOrder.append(forum["_id"])

	# Re-order categories and forums
	c = 0
	f = 0

	for elem in newOrdering:
		if "Category" in elem:
			colCategories.find_one_and_update({"_id":catOrder[int(elem[8:])]}, {"$set":{"order":c}})
			print("   "+elem+" ("+str(catOrder[int(elem[8:])])+") -> "+str(c))
			c += 1
			f = 0
		elif "Forum" in elem:
			colForums.find_one_and_update({"_id":forumsOrder[int(elem[5:])]}, {"$set":{"order":f}})
			print("   "+elem+" ("+str(forumsOrder[int(elem[5:])])+") -> "+str(f))
			f += 1

	return "/admin"