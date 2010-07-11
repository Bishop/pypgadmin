import re
import template as tpl
import base

SOFTWARE_NAME = 'pythonPgAdmin'
SOFTWARE_VERSION = '0.0.1'

urls = [
	(r'^$', 'index'),
	(r'^record(?:/(\d+))?$', 'record'),
	(r'^env', 'show_environment'),
	(r'^Debug/?$', 'show_environment'),
]

def show_environment(environ, start_response):
	response_body = ['%s: %s\n<br>\n' % (key, value) for key, value in sorted(environ.items())]
	start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])

	return response_body


def not_found(environ, start_response):
	""" 404 """
	start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
	return ['Not found']

def index(environ, start_response):
	""" Display index page """
	start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])

	template = tpl.Template('templates/index.html')

	connections_template = tpl.Template('templates/b.connection.html')
	connections = base.Connections()
	for name in connections.list_connection():
		options = connections.get_connection_params(name)
		options['name'] = name
		connections_template.block(options)

	context = {
		'software_name': SOFTWARE_NAME,
		'software_version': SOFTWARE_VERSION,
		'message': 'Hello, world',
		'connections': connections_template.render()
	}
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


