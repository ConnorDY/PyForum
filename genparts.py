from loadtemplates import loadTemplates

import time
import datetime

def genTop(title):
	temps = loadTemplates(["top", "header"])
	
	return temps["top"].format(header=temps["header"],pageTitle=title)

def genBottom(ts):
	temps = loadTemplates(["bottom"])

	r_time = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S %m/%d/%Y")
	r_elapsed = time.time()-ts

	return temps["bottom"].format(time=r_time,elapsed=r_elapsed)