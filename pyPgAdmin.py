import re
import json
import base

from jinja2 import Environment, PackageLoader

SOFTWARE_NAME = 'pyPgAdmin'
SOFTWARE_VERSION = '0.0.2'

env = Environment(loader=PackageLoader(SOFTWARE_NAME, 'templates'))

urls = [
	(r'^$', 'index'),
	(r'^init$', 'init'),
	(r'^Debug$', 'show_environment'),
	(r'^SQLConsole$', 'show_sqlconsole'),

	(r'^db/(?P<dbname>\w+)/(?P<profile>\w+)/schema/(?P<schema>\w+)/table/(?P<table>[^/]+)(?:/(?P<show>\w+))?$', 'show_table'),

	(r'^db/(?P<profile>\w+)$', 'get_databases'),
	(r'^db/(?P<dbname>\w+)/(?P<profile>\w+)$', 'get_schemas'),
	(r'^db/(?P<dbname>\w+)/(?P<profile>\w+)/schema/(?P<schema>\w+)$', 'get_tables'),

	(r'^page/(?P<profile>\w+)$', 'show_page'),
]

class Application(object):
	environ = None
	start_response = None
	def __call__(self, environ, start_response):
		return self.dispatch_request(environ, start_response)

	def dispatch_request(self, environ, start_response):
		self.environ = environ
		self.start_response = start_response

		path = environ.get('PATH_INFO', '').strip('/')

		for regex, callback in urls:
			match = re.search(regex, path)
			if match is not None:
				return getattr(self, callback)(**match.groupdict())
		else:
			return self.not_found()

	def not_found(self):
		""" 404 """
		self.start_response('404 NOT FOUND', [('Content-Type', 'text/plain')])
		return ['Not found']


	def get_databases(self, profile):
		c = self.connection_params(profile)
		dbm = base.DataBaseManager(**c)
		self.start_response('200 OK', [('Content-Type', 'application/json; charset=utf-8')])

		return json.JSONEncoder().encode([db.datname for db in dbm.get_databases()])


	def show_environment(self):
		response_body = ['%s: %s\n<br>\n' % (key, value) for key, value in sorted(self.environ.items())]
		self.start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])

		return response_body


	def index(self):
		""" Display index page """
		self.start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])

		template = env.get_template('index.html')

		connections = base.Connections()
		connection_options = list()
		for name in connections.list_connection():
			options = connections.get_connection_params(name)
			options['name'] = name
			connection_options.append(options)

		return template.render(connections=connection_options, message='Hello, world').encode('utf8')

	def init(self):
		""" Return initialization information about application """

		self.start_response('200 OK', [('Content-Type', 'application/json; charset=utf-8')])

		application = {
			'name': SOFTWARE_NAME,
			'version': SOFTWARE_VERSION,
			'config': {
				'connections': []
			}
		}

		return json.JSONEncoder().encode(application)

	def connection_params(self, profile, dbname = None):
		dbc = base.Connections().get_connection_params(profile)
		if dbname is not None:
			dbc['dbname'] = dbname
		return dbc

	def show_table(self, profile, dbname, schema, table, show):
		connection = self.connection_params(profile, dbname)
		dbm = base.DataBaseManager(**connection)
		self.start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])

		if show == 'data':
			tbl = dbm.get_table_data(schema, table)
			template = env.get_template('table.data.html')
		else:
			tbl = dbm.get_table_structure(schema, table)
			template = env.get_template('table.structure.html')

		types = dbm.get_types()

		result = template.render(table=tbl, table_info={'table': table, 'dbname': dbname, 'schema': schema}, types=types, connection=connection)
		return result.encode("utf8")

	def get_tables(self, profile, dbname, schema):
		dbm = base.DataBaseManager(**self.connection_params(profile, dbname))
		self.start_response('200 OK', [('Content-Type', 'application/json; charset=utf-8')])
		return json.JSONEncoder().encode(dbm.get_tables(schema))

	def get_schemas(self, profile, dbname):
		dbm = base.DataBaseManager(**self.connection_params(profile, dbname))
		self.start_response('200 OK', [('Content-Type', 'application/json; charset=utf-8')])
		return json.JSONEncoder().encode(dbm.get_schemas())

	def show_page(self, profile):
		self.start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
		connection = self.connection_params(profile)
		dbm = base.DataBaseManager(**connection)
		dbs = dbm.get_databases()
		template = env.get_template('conn.databases.html')
		return template.render(databases=dbs, connection=connection).encode("utf8")