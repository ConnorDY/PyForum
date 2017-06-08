# path="/admin"

from pymongo import MongoClient
from bson.objectid import ObjectId
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

	if len(args) != 1:
		return "/admin"

	from functions import checkFieldsBlank

	args["0"] = "" # add new key so the following checks work

	# Re-order categories and/or forums
	if "reorder" in args:
		# Make sure values entered are alright
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

	# Add new category
	elif "newCat" in args:
		# Make sure values entered are alright
		fields = ["name"]
		if checkFieldsBlank(form, fields):
			return "/admin"

		# Connect to Mongo DB
		client = MongoClient("mongodb://localhost:27017/")
		db = client.db
		colCategories = db.categories

		newCat = {
			"title": form["name"].value,
			"order": colCategories.count()
		}

		# Add the new category to the database
		colCategories.insert(newCat)
		print("New forum category added: "+form["name"].value)

	# Add new forum
	elif "newForum" in args:
		# Make sure values entered are alright
		fields = ["name", "category", "desc"]
		if checkFieldsBlank(form, fields):
			return "/admin"

		# Connect to Mongo DB
		client = MongoClient("mongodb://localhost:27017/")
		db = client.db
		colCategories = db.categories
		colForums = db.forums

		# Check if the selected category exists
		if colCategories.find_one({"_id":ObjectId(form["category"].value)}) != None:
			# Get number of forums in that category
			count = colForums.find({"cat":ObjectId(form["category"].value)}).count()

			newForum = {
				"cat": ObjectId(form["category"].value),
				"order": count,
				"name": form["name"].value,
				"desc": form["desc"].value,
				"numThreads": 0,
				"numPosts": 0
			}

			colForums.insert(newForum)
			print("New forum added to \""+form["category"].value+"\": "+form["name"].value)

	return "/admin"