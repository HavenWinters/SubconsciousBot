def prettyPrintListOfDice(listItems:list):
		return f'Rolled {str(listItems)} Sum: {sum(listItems)}'


def prettyPrintCommands(commands):
	s = ''
	for command in commands:
		s = f'{s}\n{command}:: {commands[command]["total"]}'
	return s