
class Template(object):
	_content_ = None
	
	def __init__(self, filename=''):
		if filename != '':
			self.load(filename)

	def load(self, filename):
		with open(filename, 'r') as f:
			self._content_ = f.read()

	def render(self, context):
		return self._content_ % context