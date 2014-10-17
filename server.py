# Modules
import http.server
import socketserver

import os.path
import time
import cgi

import pagegetfunction

# Vars
PORT = 80
HTML = 0
IMG = 1
CSS = 2
JS = 3

# Custom HTTP Request Handler
class Handler(http.server.SimpleHTTPRequestHandler):
	# Headers?
	def do_HEAD(s):
		s.send_response(200)
		s.send_header("Content-type", "text/html")
		s.end_headers()

	# Handle Get Requests
	def do_GET(s):
		# Default to not redirecting
		redirect = False

		# Current timestamp
		ts = time.time()

		# Default request type
		reqType = HTML

		## Path ##
		tPath = s.path

		# Fix path if it contains a question mark
		sArgs = None

		iQ = tPath.find('?')
		if iQ != -1:
			sArgs = dict(itm.split('=',1) for itm in tPath[iQ+1:].split('&'))
			#sArgs = dict((itm.split('=')[0],itm.split('=')[1]) for itm in tPath[iQ+1:].split('&'))
			#sArgs = tPath[iQ+1:]
			tPath = tPath[:iQ]

		# Index Page
		if tPath == "/":
			path = "/index"
		else:
			# Images
			if tPath.endswith(".gif") or tPath.endswith(".png") or tPath.endswith(".jpeg") or tPath.endswith(".jpg"):
				path = tPath[1:] # Cut off leading forward slash
				reqType = IMG

			# CSS Stylesheets
			elif tPath.find("/css/") == 0:
				path = tPath[1:] # Cut off leading forward slash
				reqType = CSS

			# Javascript
			elif tPath.find("/js/") == 0:
				path = tPath[1:] # Cut off leading forward slash
				reqType = JS

			# HTML Pages
			elif os.path.isfile("html" + tPath + ".html"):
				path = tPath

			# 404: Page not found
			else:
				path = "/404"

		## Get Page Contents ##
		if reqType == IMG:
			with open (path, "rb") as file:
				r = file.read()
		elif reqType == CSS or reqType == JS:
			with open (path, "r") as file:
				r = file.read()
		else:
			with open ("html"+path+".html", "r") as file:
				r = file.read()


		## Import page's GET method ##
		func = pagegetfunction.get(path)

		# Run page get function if it exists
		if func is not None:
			r = func(ts, r, sArgs, s)


		## Response Codes ##
		if redirect:
			s.send_response(301)
		elif path != "/404":
			s.send_response(200)
		else:
			s.send_response(404)


		## Headers ##

		# HTML
		if reqType == HTML:
			s.send_header("Content-type", "text/html")
			r = r.encode("utf-8")

		# Javascript
		elif reqType == JS:
			s.send_header("Content-type", "text/javascript")
			r = r.encode("utf-8")

		# CSS Stylesheets
		elif reqType == CSS:
			s.send_header("Content-type", "text/css")
			r = r.encode("utf-8")

		# Images
		elif reqType == IMG:
			cType = ""

			# PNG
			if path.endswith(".png"):
				cType = "png"
			# JPEG
			elif path.endswith(".jpeg") or path.endswith(".jpg"):
				cType = "jpeg"
			# GIF
			elif path.endswith(".gif"):
				cType = "gif"

			s.send_header("Content-type", "image/"+cType)

		s.end_headers()


		## Page Content ##
		s.wfile.write(r)
		s.wfile.flush()

	# Handle Post Requests
	def do_POST(s):
		# Get POST data
		form = cgi.FieldStorage(
			fp=s.rfile,
			headers=s.headers,
			environ={"REQUEST_METHOD":"POST",
					"CONTENT_TYPE":s.headers["Content-Type"],
					})

		# Response
		s.send_response(301)

		## Import page's POST module ##
		func = pagegetfunction.post(s.path)
		
		loc = None

		# Pass POST data to page
		if func is not None:
			loc = func(s, form)

		# Send headers
		s.send_header("Location", loc)
		s.end_headers()

		

# Create TCP HTTP Server
httpd = socketserver.TCPServer(("", PORT), Handler)

print("serving at port", PORT)

try:
	httpd.serve_forever()
except KeyboardInterrupt:
	pass
httpd.server_close()