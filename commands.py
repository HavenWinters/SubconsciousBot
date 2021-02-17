

class Command():

	def __init__(self,name:str, advType:int=0,intensity:int=0) -> None:	
		if isinstance(name,str):
			self.name = name 
		else:
			raise TypeError('Name needs to be a string')
		self.advType = advType
		self.intensity = intensity

	@property
	def intensity(self) -> int:
		return self.__intensity
	
	@intensity.setter
	def intensity(self,value:int) -> None:
		if value >= 0:
			self.__intensity = value
		else:
			raise ValueError('Intensity has to be greater than or equal to 0')

	@property
	def advType(self) -> int:
		return self.__advType
	
	@advType.setter
	def advType(self,value:int) -> None:
		if value in [-1,0,1]:
			self.__advType = value
		else:
			raise ValueError('advType has to be either [-1,0,1]')


	@property
	def output(self) -> dict:
		outDict = {}
		if self.advType in [-1,1]:
			outDict['advType'] = self.advType
			# setattr(outDict,'advType',)
		if self.intensity > 0:
			# setattr(outDict,'intensity',self.intensity)
			outDict['intensity'] = self.intensity
		return outDict


def parseCommandsDict(commandsDict:dict = None) -> list:
	commandsList = []
	if commandsDict == None:
		return commandsList
	else:
		for name, value in commandsDict.items():
			advType = value.get('advType',0)
			intensity = value.get('intensity',0)
			commandsList.append(Command(name,advType,intensity))
	return commandsList

def constructCommandsDict(commandsList:list = []) -> dict:
	commandsDict = {}
	for command in commandsList:
		commandsDict[command.name] = command.output
	return commandsDict
# class GroupedCommands():

# 	def __init__(self,commandsDict:dict = None):
# 		'''
# 		Input a dictionary of commands to be operated on.
# 		Each Command is of the form
# 		name:{advType:1,intensity:0}
# 		'''
# 		if commandsDict == None: #mutable dictionaries makes this pattern necessary
# 			self.commandsDict = {}
# 		else:
# 			self.commandsDict = commandsDict

# 		self.commandList = parseCommandsDict(self.commandsDict)



if __name__ == '__main__':
	import unittest

	class testCommand(unittest.TestCase):

		def test_commandCreation(self):
			c = Command('TestingName')
			self.assertEqual(c.name, 'TestingName')
			self.assertEqual(c.advType, 0)
			self.assertEqual(c.intensity, 0)

		def test_output_noDefaultValues(self):
			c = Command('TestingName')
			out = c.output
			self.assertTrue(isinstance(out,dict))
			self.assertFalse('advType' in out.keys())
			self.assertFalse('intensity' in out.keys())

		def test_output_nonDefaultValues(self):
			c = Command('TestingName',1,100)
			out = c.output
			self.assertTrue(isinstance(out,dict))
			self.assertEqual(out['advType'], 1)
			self.assertEqual(out['intensity'], 100)

		def test_negativeIntensity(self):
			with self.assertRaises(ValueError):
				_ = Command('TestingName',1,-1)

			c = Command('TestingName',1,100)
			with self.assertRaises(ValueError):
				c.intensity = -100

		def test_advType_valueError(self):
			with self.assertRaises(ValueError):
				_ = Command('TestingName',3,-1)

			c = Command('TestingName',1,100)
			with self.assertRaises(ValueError):
				c.advType = -10


	class testparseCommandsDict(unittest.TestCase):

		def test_emptyDict(self):
			self.assertIsInstance(parseCommandsDict({}),list)
			self.assertIsInstance(parseCommandsDict(),list)
			
		def test_commandsConvertToList(self):
			l = parseCommandsDict({'a':{'intensity':50}})
			self.assertEqual(l[0].name,'a')
			self.assertEqual(l[0].advType,0)
			self.assertEqual(l[0].intensity,50)

		def test_constructParsed(self):
			commandDict = {'a':{'intensity':50}}
			p = parseCommandsDict(commandDict)
			self.assertEqual(constructCommandsDict(p),commandDict)




	unittest.main()