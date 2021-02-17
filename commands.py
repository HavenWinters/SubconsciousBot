import dice

class Command():

	def __init__(self,name:str, advType:int=0,intensity:int=0) -> None:	
		if isinstance(name,str):
			self.name = name 
		else:
			raise TypeError('Name needs to be a string')
		self.advType = advType
		self.intensity = intensity
		self.rolled = (0,0) # (roll,outof) 

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
	def stringAdvType(self) -> str:
		return ['dis','nat','adv'][self.advType + 1]

	def roll(self,rollFor:int) -> int:
		self.rolled = (dice.rollGivenAdvType(self.stringAdvType,rollFor),rollFor)
		return self.rolled[1]

	@property
	def output(self) -> dict:
		outDict = {}
		if self.advType in [-1,1]:
			outDict['advType'] = self.advType
		if self.intensity > 0:
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


def increaseIntensity(commandList:list, addsUpTo:int) -> list:
	'''Increases The users command totals by a rolled amount that cumulativly adds up to the input addsUpTo.
		Example:
		assume you wanted the values to add up to 20
		assume you rolled 10,5 then the scaling factor was 4/3
		you would have 10,15 as your cumulative results
		you would then have 13,20 as your cumulative scaled results
		finding the differences with the previous values gives you 13,7
	'''
	if commandList == []:
		return commandList
	cumulativeTotal = 0
	cumulativeTotalList = []
	### In Order to scale everything appropriately everything is converted to cumulative.
	for command in commandList:
		cumulativeTotal = cumulativeTotal + command.roll(20)
		cumulativeTotalList.append(cumulativeTotal)

	if cumulativeTotal <= 0:
		raise ZeroDivisionError('cumulativeTotal should never be less than or equal to 0.')
	### In order to get the multiplier to be correct it has to be a float however
	### that will cause problems down the line. 
	### This is where the cumulative comes intopractice.
	overallScalingFactor = addsUpTo / cumulativeTotal
	prevRoll = 0
	for cumulativeTotal,command in zip(cumulativeTotalList,commandList):
		### Every roll is scaled by the overall scaling factor and then rounded to integer
		scalingRoll = round(cumulativeTotal * overallScalingFactor)
		### scaling roll - previous roll is the key to all of this.
		### because they are both cumulative and scaled and rounded the difference between
		### them is the actual scaled up roll that takes account of rounding

		### The rest of the line makes sure that the total is greater than or equal to 0
		### And makes sure that the new scaled result gets added to the previous total
		command.intensity = max(0,( command.intensity + scalingRoll - prevRoll ))
		### Setting the prevRoll to the current set of rolls after it has been used
		### Essentially turns this into a lag function where it is looking at the previous roll
		prevRoll = scalingRoll
	return commandList

class GroupedCommands():

	def __init__(self,commandsDict:dict = None):
		'''
		Input a dictionary of commands to be operated on.
		Each Command is of the form
		name:{advType:1,intensity:0}
		'''
		if commandsDict == None: #mutable dictionaries makes this pattern necessary
			self.commandsDict = {}
		else:
			self.commandsDict = commandsDict

		self.commandList = parseCommandsDict(self.commandsDict)

	@property
	def output(self) -> dict:
		return {command.name: command.output for command in self.commandList}

	def increase(self,amount) -> None:
		increaseIntensity(self.commandList,amount)

	def addCommand(self,newCommand:Command) -> None:
		if newCommand.name in [command.name for command in self.commandList]:
			raise Exception('Cannot create a new command with the same name')
		else:
			self.commandList.append(newCommand)

	def deleteCommand(self,name:str) -> None:
		tempDict = self.output
		try:
			del tempDict[name]
		except:
			raise Exception('Cannot delete command')
		finally:
			self.commandList = parseCommandsDict(tempDict)







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


	class testIncreaseIntensity(unittest.TestCase):

		def test_emptyList(self):
			self.assertIsInstance(increaseIntensity([],100),list)
			self.assertEqual(increaseIntensity([],100),[])

		def test_increaseOneCommandByN(self):
			cmds = [Command('Testing',0,0)]
			self.assertEqual(cmds[0].intensity,0)
			cmds2 = increaseIntensity(cmds,100)
			self.assertEqual(cmds[0].intensity,100) # mutates collection of commands
			self.assertEqual(cmds2[0].intensity,100)

		def test_increaseMultipleByN(self):
			cmds = [Command('Testing',0,30),Command('Testing2',0,20)]
			self.assertEqual(sum(command.intensity for command in cmds),50)
			cmds = increaseIntensity(cmds,100)
			self.assertEqual(sum(command.intensity for command in cmds),150)


	class testGroupedCommands(unittest.TestCase):

		def test_addCommand(self):
			gc = GroupedCommands({})
			gc.addCommand(Command('Testing'))
			self.assertEqual(gc.commandList[0].name,'Testing')
			gc.addCommand(Command('Bob'))
			self.assertEqual(gc.commandList[1].name,'Bob')

		def test_delCommand(self):
			gc = GroupedCommands({'Testing':{},'Bob':{}})
			self.assertEqual(gc.commandList[0].name,'Testing')
			self.assertEqual(gc.commandList[1].name,'Bob')
			gc.deleteCommand('Testing')
			self.assertEqual(gc.commandList[0].name,'Bob')
			self.assertEqual(len(gc.commandList),1)
			gc.deleteCommand('Bob')
			self.assertEqual(len(gc.commandList),0)

		def test_output(self):
			input = {'Testing':{},'Bob':{'intensity':100}}
			gc = GroupedCommands(input)
			self.assertEqual(gc.output,input)

		def test_increaseIntensity(self):
			input = {'Testing':{},'Bob':{'intensity':100}}
			gc = GroupedCommands(input)
			gc.increase(50)
			self.assertEqual(sum(command.intensity for command in gc.commandList),150)








	unittest.main()