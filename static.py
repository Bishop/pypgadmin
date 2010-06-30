import os

class StaticFilesFilter(object):
	def __init__(self, application):
		self.app = application

	def __call__(self, environ, start_response):
		file_path = environ["PATH_INFO"][1:]
		if not os.path.isfile(file_path):
			return self.app(environ, start_response)

		start_response("200 OK", [])

		return self.send_file(file_path)

	def send_file(self, file_path):
		with open(file_path) as f:
			block = f.read(4096)
			while block:
				yield block
				block = f.read(4096)