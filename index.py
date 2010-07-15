import sys

sys.path.append(r'd:/web/docs/pass/')

import pyPgAdmin
import static

def application(environ, start_response):
	return pyPgAdmin.dispatch_request(environ, start_response)

def factory():
	return static.StaticFilesFilter(application)

if __name__ == '__main__':
	from  wsgiref.simple_server import make_server
	srv = make_server('localhost', 8090, factory())
	srv.serve_forever()
