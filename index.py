import sys

sys.path.append(r'd:/web/docs/pass/')

import pass_app

def application(environ, start_response):
	return pass_app.dispatch_request(environ, start_response)

if __name__ == '__main__':
	from  wsgiref.simple_server import make_server
	srv = make_server('localhost', 8090, application)
	srv.serve_forever()
