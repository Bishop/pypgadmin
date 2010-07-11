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
	def __init__(self, info):
		(self.catalog, self.schema, self.name, ) = info[:3]

class DataBaseManager(object):

	def __init__(self, user, password, host='localhost', port=5432, dbname=''):
		self.connect = psycopg2.connect(user=user, password=password, host=host, port=port, database=dbname)
		self.version = self.get_version()

	def __del__(self):
		self.connect.close()

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
		c = self.connect.cursor()
		c.execute(s)
		tablespaces = [dbTablespaceInfo(t) for t in c.fetchall()]
		c.close()
		return [t.spcname for t in tablespaces]

	def get_tables(self, schema):
		s = "SELECT * FROM information_schema.tables WHERE table_schema = %(schema)s"
		c = self.connect.cursor()
		c.execute(s, {'schema': schema})
		schemas = [dbTableInfo(t).name for t in c.fetchall()]
		c.close()
		return schemas

if __name__ == '__main__':
	connections = Connections()
	options = connections.get_connection_params(connections.list_connection()[0])
	dbm = DataBaseManager(**options)
	print "{0} {1}".format(dbm.version.version['name'], dbm.version.version['version'])
	print dbm.get_databases()
	print dbm.get_schemas()
	print dbm.get_tablespaces()
	print dbm.get_tables('software')