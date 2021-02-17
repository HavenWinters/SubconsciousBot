

class Command():

	def __init__(self,name:str, advType:int=0,intensity:int=0) -> None:
		self.name = name
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
		outDict = {'name':self.name}
		if self.advType in [-1,1]:
			outDict['advType'] = self.advType
			# setattr(outDict,'advType',)
		if self.intensity > 0:
			# setattr(outDict,'intensity',self.intensity)
			outDict['intensity'] = self.intensity
		return outDict




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
			self.assertEqual(out['name'], 'TestingName')
			self.assertFalse('advType' in out.keys())
			self.assertFalse('intensity' in out.keys())

		def test_output_nonDefaultValues(self):
			c = Command('TestingName',1,100)
			out = c.output
			self.assertTrue(isinstance(out,dict))
			self.assertEqual(out['name'], 'TestingName')
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



	unittest.main()