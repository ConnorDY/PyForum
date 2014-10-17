# path="/index"

from pymongo import MongoClient

import time
import datetime

def get(ts, r, args):
	# Current date and time
	r_time = datetime.datetime.fromtimestamp(ts).strftime("%Y/%m/%d %H:%M:%S")

	# Table
	r_table = "<tr><th>Message</th><th>Time</th></tr>";

	# Connect to Mongo DB
	client = MongoClient("mongodb://localhost:27017/")
	db = client.db
	col = db.messages

	# Retrieve and display messages
	for msg in col.find().sort("_id", -1):
		r_table += "<tr><td>{}</td><td>{}</td></tr>\n".format(
			msg["message"],
			datetime.datetime.fromtimestamp(msg["time"]).strftime("%H:%M:%S")
		)

	# Time it took to generate this page
	r_elapsed = time.time()-ts

	# Return modified template
	return r.format(table=r_table,time=r_time,elapsed=r_elapsed)

def post(s, form):
	# Connect to Mongo DB
	client = MongoClient("mongodb://localhost:27017/")
	db = client.db
	col = db.messages

	# Insert message into database
	msg = {"message": form["message"].value,
		   "time": time.time()}
	col.insert(msg)

	print("Message was posted to chat: {}".format(form["message"].value))

	return "/index"