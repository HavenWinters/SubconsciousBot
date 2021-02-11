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
		# finished deleting so add the new Data
		db[self.key] = newData
	
	def updateSubKey(self,subKey,newValue):
		'''
		For a key in the returned data update the value.
		Returns a tuple with (Success:bool,Result:str)
		'''
		if self.inDB:
			try:
				getData = self.data
				prevVal = getattr(getData,subKey,f'{subKey} having no value')
				getData[subKey] = newValue
				self.equals(getData)
				return (True, f'{subKey} updated from {str(prevVal)} to {newValue}')
			except:
				return (False,'Error: Unknown Error with the update.')
		else:
			return (False,'Error: Nothing in DB. Please Add.')