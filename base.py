import psycopg2
import re
import ConfigParser

class Connections(object):
	file = 'connections.cfg'
	def __init__(self):
		config = ConfigParser.RawConfigParser()
		config.read(self.file)
		self.connections = dict([(section, dict(config.items(section))) for section in config.sections()])
	def set_connection(self, name, user, password, host='localhost', port=5432, dbname=''):
		self.connections[name] = {'user': user, 'password': password, 'host': host, 'port': port, 'dbname': dbname}
	def list_connection(self):
		return self.connections.keys()
	def get_connection_params(self, connection):
		return self.connections[connection]
	def write(self):
		config = ConfigParser.RawConfigParser()
		for section in self.connections:
			config.add_section(section)
			for option in self.connections[section]:
				config.set(section, option, self.connections[section][option])
		with open(self.file, 'wb') as config_file:
			config.write(config_file)


class dbDBInfo(object):
	def __init__(self, info):
		(self.datname, self.datdba, self.encoding, ) = info[:3]

class dbVersion(object):
	def __init__(self, info):
		self.version_str = info[0]
		m = re.match(r'^(?P<name>\w+) (?P<version>(?P<major>\d+)(?:\.(?P<minor>\d+))?(?:\.(?P<build>\d+))?), (?P<notes>.*?)(?:, (?P<arch>\d+)-bit)?$', "PostgreSQL 8.4.2, compiled by Visual C++ build 1400, 32-bit")
		self.version = m.groupdict()

class dbSchemaInfo(object):
	def __init__(self, info):
		(self.catalog, self.schema, self.owner, ) = info[:3]

class dbTablespaceInfo(object):
	def __init__(self, info):
		self.spcname = info[0]

class dbTableInfo(object):
	def __init__(self, info=None):
		if info is not None:
			(self.catalog, self.schema, self.name, ) = info[:3]

class dbColumnInfo(object):
	def __init__(self, info):
		(self.table_name, self.column_name) = info[2:4]
		(self.column_default, self.is_nullable, self.data_type, self.char_max) = info[5:9]
		self.udt_name = info[27]

		self.char_max = self.char_max or ''
	def get_dict(self):
		return self.__dict__
	def __repr__(self):
		return repr(self.__dict__)

class DataBaseManager(object):

	def __init__(self, user, password, host='localhost', port=5432, dbname=''):
		self.connect = psycopg2.connect(user=user, password=password, host=host, port=port, database=dbname)
		self.version = self.get_version()

	def __del__(self):
		self.connect.close()

	def query(self, sql, params=None):
		c = self.connect.cursor()
		c.execute(sql, params)
		result = {'header': c.description, 'body': c.fetchall()}
		c.close()
		return result

	def get_databases(self):
		""" Returns names of all databases """
		s = "SELECT * FROM pg_database WHERE NOT datistemplate"
		c = self.connect.cursor()
		c.execute(s)
		dbs = [dbDBInfo(x) for x in c.fetchall()]
		c.close()
		return [dbinfo.datname for dbinfo in dbs]

	def get_version(self):
		""" Return version of database """
		c = self.connect.cursor()
		c.execute("SELECT version()")
		version = c.fetchone()
		c.close()
		return dbVersion(version)

	def get_schemas(self, show_system=False):
		s = "SELECT * FROM information_schema.schemata ORDER BY schema_name"
		c = self.connect.cursor()
		c.execute(s)
		schemas = [dbSchemaInfo(s) for s in c.fetchall() if show_system or not s[1].startswith('pg_')]
		c.close()
		return [s.schema for s in schemas]

	def get_tablespaces(self):
		s = "SELECT * FROM pg_tablespace ORDER BY spcname"
		tablespaces = [dbTablespaceInfo(t) for t in self.query(s)['body']]
		return [t.spcname for t in tablespaces]

	def get_tables(self, schema):
		s = "SELECT * FROM information_schema.tables WHERE table_schema = %(schema)s ORDER BY table_name"
		return [dbTableInfo(t).name for t in self.query(s, {'schema': schema})['body']]

	def get_table_structure(self, schema, table_name):
		s = """
			SELECT
				*
			FROM
				information_schema.columns
			WHERE
					table_schema = %(schema)s
				AND table_name = %(table)s
		"""
		table = dbTableInfo(('', schema, table_name))
		table.columns = [dbColumnInfo(ci) for ci in self.query(s, {'schema': schema, 'table': table_name})['body']]
		return table

	def get_table_data(self, schema, table_name, limit=100, offset=0):
		s = """
			SELECT
				*
			FROM
				%(schema)s.%(table)s
			LIMIT
				%(limit)d
			OFFSET
				%(offset)d
		"""
		s = s % {'schema': schema, 'table': table_name, 'limit': limit, 'offset': offset}
		return self.query(s)

	def get_types(self):
		s = """
			SELECT
				pg_type.*
			FROM
				pg_type
		"""
#				JOIN pg_namespace
#					ON typnamespace = pg_namespace.oid
#			WHERE
#				nspname = %(namespace)s"""
		return self.query(s)['body'] # {'namespace': 'pg_catalog'}
		

if __name__ == '__main__':
	connections = Connections()
	options = connections.get_connection_params(connections.list_connection()[0])
	dbm = DataBaseManager(**options)
	print "{0} {1}".format(dbm.version.version['name'], dbm.version.version['version'])
	print dbm.get_databases()
	print dbm.get_schemas()
	print dbm.get_tablespaces()
	schema = 'software'
	print dbm.get_tables(schema)
	print dbm.get_table_structure(schema, 'soft').columns
	print dbm.get_table_data(schema, 'soft')