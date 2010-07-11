import re
import template as tpl
import base

SOFTWARE_NAME = 'pythonPgAdmin'
SOFTWARE_VERSION = '0.0.1'

urls = [
	(r'^$', 'index'),
	(r'^Debug?$', 'show_environment'),
	(r'^SQLConsole?$', 'show_sqlconsole'),

	(r'^server/(?P<profile>\w+)', 'show_server')
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

def show_server(environ, start_response, profile):
	connections = base.Connections()
	c = connections.get_connection_params(profile)
	dbm = base.DataBaseManager(**c)
	db_template = tpl.Template('templates/b.database.html')
	for db_name in dbm.get_databases():
		db_template.block({'db_name': db_name})
	start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
	return db_template.render()

def dispatch_request(environ, start_response):
	path = environ.get('PATH_INFO', '').strip('/')
	for regex, callback in urls:
		match = re.search(regex, path)
		if match is not None:
			environ['pass.args'] = match.groups()
			return globals()[callback](environ, start_response, **match.groupdict())
	else:
		return not_found(environ, start_response)


