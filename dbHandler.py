from replit import db

class DBkey:
	def __init__(self,key):
		self.key = key

	def __repr__(self):
		return f'DBkey({self.key})'

	def __str__(self):
		return f'db["{self.key}"]\n{"-"*len(self.key)}\n{self.data}'

	@property
	def inDB(self):
		return self.data != None

	@property
	def data(self):
		try:
			return db[self.key]
		except:
			return None	

	@data.deleter
	def data(self):
		del db[self.key]

	@data.setter
	def data(self,newData):
		if self.inDB:
			del self.data
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
				self.data = getData
				return (True, f'{subKey} updated from {str(prevVal)} to {newValue}')
			except:
				return (False,'Error: Unknown Error with the update.')
		else:
			return (False,'Error: Nothing in DB. Please Add.')