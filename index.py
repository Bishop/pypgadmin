import os
import sys

sys.path.append(os.path.dirname(__file__))
os.curdir = os.path.dirname(__file__)

import pyPgAdmin
import static

#def application(environ, start_response):
#	if 'PYTHON_EGG_CACHE' in environ:
#		os.environ['PYTHON_EGG_CACHE'] = environ['PYTHON_EGG_CACHE']
#	else:
#		os.environ['PYTHON_EGG_CACHE'] = os.path.join(os.path.dirname(__file__),
#		'.egg-cache')
#
#	return pyPgAdmin.dispatch_request(environ, start_response)

def factory():
	return static.StaticFilesFilter(pyPgAdmin.Application())

if __name__ == '__main__':
	from  wsgiref.simple_server import make_server
	srv = make_server('localhost', 8090, factory())
	srv.serve_forever()
