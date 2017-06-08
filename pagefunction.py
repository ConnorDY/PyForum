def get(path):
	func = None

	# Index
	if path == "/index":
		import pg_index
		func = pg_index.get

	# View Forum
	elif path == "/viewforum":
		import pg_viewforum
		func = pg_viewforum.get

	# View Thread
	elif path == "/viewthread":
		import pg_viewthread
		func = pg_viewthread.get

	# Login
	elif path == "/login":
		import pg_login
		func = pg_login.get

	# Register
	elif path == "/register":
		import pg_register
		func = pg_register.get

	# Logout
	elif path == "/logout":
		import pg_logout
		func = pg_logout.get

	# Posting
	elif path == "/posting":
		import pg_posting
		func = pg_posting.get

	# Admin Control Panel
	elif path == "/admin":
		import pg_admin
		func = pg_admin.get

	return func

def post(path):
	func = None

	# Login
	if path == "/login":
		import pg_login
		func = pg_login.post

	# Register
	elif path == "/register":
		import pg_register
		func = pg_register.post

	# View Thread (reply)
	elif path == "/viewthread":
		import pg_viewthread
		func = pg_viewthread.post

	# Posting
	elif path == "/posting":
		import pg_posting
		func = pg_posting.post

	# Admin Control Panel
	elif path == "/admin":
		import pg_admin
		func = pg_admin.post

	return func