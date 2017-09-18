

class Keywords():

	def __init__(self,keys=None):

		if keys is None:
			keys = []

		self.keywords = keys

	def add_keyword(self,keyword):

		self.keywords.append(keyword)

	def remove_keyword(self,keyword):

		self.keywords.remove(keyword)

	def get_keywords(self):

		return self.keywords