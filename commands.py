

class Command():

	def __init__(self,name:str, advType:int=0,intensity:int=0) -> None:
		self.name = name
		self.advType = advType
		self.intensity = intensity

	@property
	def output(self):
		return {}





if __name__ == '__main__':
	import unittest

	class testCommand(unittest.TestCase):

		def test_commandCreation(self):
			c = Command('TestingName')
			self.assertEqual(c.name, 'TestingName')
			self.assertEqual(c.advType, 0)
			self.assertEqual(c.intensity, 0)

		def test_output(self):
			c = Command('TestingName')
			out = c.output
			self.assertTrue(isinstance(out,dict))


	unittest.main()