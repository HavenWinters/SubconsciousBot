from replit import db

class DB:
	def __init__(self,key):
	self.key = key

	@property
	def inDB(self):
	try:
		self.data
		return True
	except:
		return False

	@property
	def delete(self):
	del db[self.key]

	@property
	def data(self):
	return db[self.key]

	def equals(self,newData):
	if self.inDB:
		self.delete
	
	db[self.key] = newData
	
