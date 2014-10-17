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

	# Login
	elif path == "/register":
		import pg_register
		func = pg_register.get

	return func

def post(path):
	func = None

	# Register
	if path == "/register":
		import pg_register
		func = pg_register.post

	# Login
	elif path == "/login":
		import pg_login
		func = pg_login.post

	return func