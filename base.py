import psycopg2

class dbDBInfo(object):
	def __init__(self, info):
		(self.datname, self.datdba, self.encoding, ) = info[:3]

class DataBaseManager(object):

	def __init__(self, user, password, host='localhost', port=5432):
		self.connect = psycopg2.connect(user=user, password=password, host=host, port=port)

	def show_databases(self):
		s = "SELECT * FROM pg_database WHERE NOT datistemplate"
		c = self.connect.cursor()
		c.execute(s)
		dbs = [dbDBInfo(x) for x in c.fetchall()]
		c.close()
		return [dbinfo.datname for dbinfo in dbs]
	def __del__(self):
		self.connect.close()


if __name__ == '__main__':
	dbm = DataBaseManager('postgres', '1')
	print dbm.show_databases()