# Modules
import http.server
import socketserver

import os.path
import os.environ
import time
import cgi

import pagefunction

# Vars
MONGODB = os.environ["MongoDB"]
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
		redirectPg = ""

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
			tPath = tPath[:iQ]

		# Index Page
		if tPath == "/":
			path = "/index"
		elif tPath == "/admin" or tPath == "/admin/":
			redirect = True
			redirectPg = "/admin/manageForums"
			path = "/404" # kind of a hack, need to fix later
		elif tPath[0:7] == "/admin/":
			path = "/admin"
			sArgs = {"path":tPath[7:]}
		else:
			# Images
			if tPath.endswith(".gif") or tPath.endswith(".png") or tPath.endswith(".jpeg") or tPath.endswith(".jpg") or tPath.endswith(".ico"):
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
		if reqType == HTML:
			func = pagefunction.get(path)

			# Run page get function if it exists
			if func is not None:
				r = func(ts, r, sArgs, s)

				# Check for redirect
				if r.find("Redirect: ") == 0:
					redirect = True
					redirectPg = r[10:]

			
		## Response Codes ##
		if redirect:
			print("Redirecting to: {}".format(redirectPg))
			s.send_response(307)
			s.send_header("Location", redirectPg)
		elif path != "/404":
			s.send_response(200)
		else:
			s.send_response(404)


		## Content-Types ##
		if not redirect:
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


		## End Headers ##
		s.end_headers()


		## Page Content ##
		if not redirect:
			s.wfile.write(r)
			s.wfile.flush()

	# Handle Post Requests
	def do_POST(s):
		## Path ##
		tPath = s.path

		# Fix path if it contains a question mark
		sArgs = None

		iQ = tPath.find('?')
		if iQ != -1:
			sArgs = dict(itm.split('=',1) for itm in tPath[iQ+1:].split('&'))
			tPath = tPath[:iQ]

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
		func = pagefunction.post(tPath)
		loc = ""

		# Pass POST data to page
		if func is not None:
			loc = func(s, form, sArgs)

		# Send headers
		s.send_header("Location", loc)
		s.end_headers()


# Create TCP HTTP Server
httpd = socketserver.TCPServer(("", PORT), Handler)
httpd.allow_reuse_address = True

print("serving at port", PORT)

try:
	httpd.serve_forever()
except KeyboardInterrupt:
	pass
httpd.server_close()