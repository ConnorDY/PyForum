# path="/logout"

def get(ts, r, args, s):
	s.send_response(307)
	s.send_header("Set-Cookie", "username=")
	s.send_header("Set-Cookie", "password=")

	return "Redirect: /index"