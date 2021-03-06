from loadtemplates import loadTemplates
from functions import checkLogin

import time
import datetime

def genTop(title, headers, navSections):
	temps = loadTemplates(["top", "header"])

	r_navbar = ""

	if checkLogin(headers):
		r_navbar += "<a href=\"./logout\">Logout</a> - "
	else:
		r_navbar += "<a href=\"./login\">Login</a> - " 
		r_navbar += "<a href=\"./register\">Register</a> - "
	
	r_navbar += "<a href=\"./faq\">FAQ</a>"

	r_header = temps["header"].format(navbar=r_navbar)

	r_navTree = genNavTree(navSections)

	r_time = datetime.datetime.fromtimestamp(time.time()).strftime("%a %b %d, %Y %I:%M %p")
	
	return temps["top"].format(header=r_header,pageTitle=title,time=r_time,navTree=r_navTree)

def genBottom(ts):
	temps = loadTemplates(["bottom"])

	r_time = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S %m/%d/%Y")
	r_elapsed = time.time()-ts

	return temps["bottom"].format(time=r_time,elapsed=r_elapsed)

def genNavTree(sections):
	temps = loadTemplates(["navTree"])

	r_navTree = ""

	for section in sections:
		r_navTree += "&nbsp;&raquo;&nbsp;<a href=\"{}\">{}</a>".format(section["link"], section["text"])

	# DST
	r_dst = " [ <abbr title=\"Daylight Saving Time\">DST</abbr> ]"

	return temps["navTree"].format(navTree=r_navTree,dst=r_dst)