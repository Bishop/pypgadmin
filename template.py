
class Template(object):
	_content_ = None
	
	def __init__(self, filename=''):
		self.items = []
		if filename != '':
			self.load(filename)

	def load(self, filename):
		with open(filename, 'r') as f:
			self._content_ = f.read()

	def render(self, context = None):
		if context is not None:
			self.block(context)
		return "".join([(self._content_ % c) for c in self.items])

	def block(self, context):
		self.items.append(context)
