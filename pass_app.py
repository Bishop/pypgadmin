import re
import template as tpl

urls = [
	(r'^$', 'index'),
	(r'^record(?:/(\d+))?$', 'record'),
	(r'^env', 'show_environment')
]

def show_environment(environ, start_response):
	response_body = ['%s: %s\n' % (key, value) for key, value in sorted(environ.items())]
	start_response('200 OK', [('Content-Type', 'text/plain')])

	return response_body


def not_found(environ, start_response):
	""" 404 """
	start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
	return ['Not found']

def index(environ, start_response):
	""" Display index page """
	start_response('200 OK', [('Content-Type', 'text/html')])

	template = tpl.Template('templates/index.html')
	context = {'message': 'Hello, world'}
	return [template.render(context)]

def record(environ, start_response):
	pass

def dispatch_request(environ, start_response):
	path = environ.get('PATH_INFO', '').lstrip('/')
	for regex, callback in urls:
		match = re.search(regex, path)
		if match is not None:
			environ['pass.args'] = match.groups()
			return globals()[callback](environ, start_response)
	else:
		return not_found(environ, start_response)
