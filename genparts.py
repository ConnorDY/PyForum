from loadtemplates import loadTemplates

import checklogin

import time
import datetime

def genTop(title, headers):
	temps = loadTemplates(["top", "header"])

	r_navbar = ""

	if checklogin.checkLogin(headers):
		r_navbar += "<a href=\"./logout\">Logout</a> - "
	else:
		r_navbar += "<a href=\"./login\">Login</a> - " 
		r_navbar += "<a href=\"./register\">Register</a> - "
	
	r_navbar += "<a href=\"./faq\">FAQ</a>"

	r_header = temps["header"].format(navbar=r_navbar)
	
	return temps["top"].format(header=r_header,pageTitle=title)

def genBottom(ts):
	temps = loadTemplates(["bottom"])

	r_time = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S %m/%d/%Y")
	r_elapsed = time.time()-ts

	return temps["bottom"].format(time=r_time,elapsed=r_elapsed)