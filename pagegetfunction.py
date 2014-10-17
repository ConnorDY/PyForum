def get(path):
	func = None

	# Index
	if path == "/index":
		import pg_index
		func = pg_index.get

	# Test Index
	elif path == "/index_":
		import pg_index_
		func = pg_index_.get

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

	# Test Index
	if path == "/index_":
		import pg_index_
		func = pg_index_.post

	# Register
	if path == "/register":
		import pg_register
		func = pg_register.post

	# Login
	if path == "/login":
		import pg_login
		func = pg_login.post

	return func