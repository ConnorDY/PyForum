# path="/viewforum"

from pymongo import MongoClient
from bson.objectid import ObjectId

from loadtemplates import loadTemplates
import genparts

def get(ts, r, args, s):
	# Connect to Mongo DB
	client = MongoClient("mongodb://localhost:27017/")
	db = client.db
	#colCategories = db.categories
	colForums = db.forums
	colThreads = db.threads

	# Load Top Template
	temps = loadTemplates(["thread"])

	# Get Forum Name
	forum = colForums.find_one({"_id": ObjectId(args["f"])})
	r_forumName = forum["name"]
	r_numThreads = forum["numThreads"]

	# Generate Top
	r_top = genparts.genTop("View Forum | " + r_forumName, s.headers)

	# Generate Navigation Tree
	sections = []
	sections.append(dict(text=forum["name"], link="viewforum?f={}".format(args["f"])))
	r_navTree = genparts.genNavTree(sections)

	# Generate Page
	r_threads = ""

	for thread in colThreads.find({"forum": ObjectId(args["f"])}).sort("order", 1):
		r_threads += temps["thread"].format(tid=thread["_id"],title=thread["title"],author=thread["author"],numReplies=thread["numReplies"],numViews=thread["numViews"],lastPost="")


	# Generate Bottom
	r_bottom = genparts.genBottom(ts)

	# Return modified template
	return r.format(threads=r_threads,top=r_top,navTree=r_navTree,bottom=r_bottom,forumName=r_forumName,fid=args["f"],numThreads=r_numThreads)