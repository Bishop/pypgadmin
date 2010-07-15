import re
import template as tpl
import base

SOFTWARE_NAME = 'pythonPgAdmin'
SOFTWARE_VERSION = '0.0.2'

urls = [
	(r'^$', 'index'),
	(r'^Debug?$', 'show_environment'),
	(r'^SQLConsole?$', 'show_sqlconsole'),

	(r'^server/(?P<profile>\w+)', 'show_server'),
	(r'^db/(?P<dbname>\w+)/(?P<profile>\w+)$', 'show_database'),
	(r'^db/(?P<dbname>\w+)/schema/(?P<schema>\w+)/(?P<profile>\w+)$', 'show_schema'),
	(r'^db/(?P<dbname>\w+)/schema/(?P<schema>\w+)/table/(?P<table>[^/]+)/(?P<profile>\w+)$', 'show_table'),
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

def connection_params(profile, dbname = None):
	dbc = base.Connections().get_connection_params(profile)
	if dbname is not None:
		dbc['dbname'] = dbname
	return dbc

def show_table(environ, start_response, dbname, schema, table, profile):
	dbm = base.DataBaseManager(**connection_params(profile, dbname))
	start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
	tbl = dbm.get_table_structure(schema, table)
	template = tpl.Template('templates/b.table.field.html')
	for field in tbl.columns:
		template.block(field.get_dict())
	rows = template.render()
	template = tpl.Template('templates/b.table.structure.html')
	return template.render({'structure': rows, 'schema': schema, 'table': table})

def show_schema(environ, start_response, dbname, schema, profile):
	dbm = base.DataBaseManager(**connection_params(profile, dbname))
	start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
	ttpl = tpl.Template('templates/b.table.html')
	for table in dbm.get_tables(schema):
		ttpl.block({'table_name': table})
	return ttpl.render()

def render_schema(dbm):
	stpl = tpl.Template('templates/b.schema.html')
	for schema in dbm.get_schemas():
		stpl.block({'schema_name': schema})
	return stpl.render()

def show_database(environ, start_response, dbname, profile):
	dbm = base.DataBaseManager(**connection_params(profile, dbname))
	start_response('200 OK', [('Content-Type', 'text/html; charset=utf-8')])
	return render_schema(dbm)

def show_server(environ, start_response, profile):
	c = connection_params(profile)
	dbm = base.DataBaseManager(**c)
	db_template = tpl.Template('templates/b.database.html')
	for db_name in dbm.get_databases():
		context = {'db_name': db_name, 'schemas': render_schema(dbm) if db_name == c['dbname'] else ''}
		db_template.block(context)
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


