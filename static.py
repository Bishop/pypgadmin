import os

class StaticFilesFilter(object):
	content_types = {
		'css': 'text/css; charset=utf-8',
		'js': 'text/javascript; charset=utf-8',
		'png': 'image/png',
		'ico': 'image/x-icon'
	}

	def __init__(self, application):
		self.app = application

	def __call__(self, environ, start_response):
		file_path = environ["PATH_INFO"][1:]
		if not os.path.isfile(file_path):
			return self.app(environ, start_response)


		start_response("200 OK", [('Content-Type', self.content_types[os.path.splitext(file_path)[1][1:]])])

		return self.send_file(file_path)

	def send_file(self, file_path):
		with open(file_path, 'rb') as f:
			block = f.read(4096)
			while block:
				yield block
				block = f.read(4096)