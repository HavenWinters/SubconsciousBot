import hypno
import dbHandler


def msgToCaller(msg):
  """This will be used to add a command"""
  listOfValidUsers = dbHandler.getUsers()
  dictValidCommands = {}
  dictValidCommands['$addCommand'] = hypno.addCommand
  dictValidCommands['$getCommand'] = hypno.currentHypnoAsString
  dictValidCommands['$rollCommand'] = hypno.callRollHypno
  dictValidCommands['$addUser'] = dbHandler.addUser

  try:
    ## split the text up into parts
    listItems = msg.content.split(" ")
    callingCommand = listItems[0]
    userName = f'{msg.guild.id} {listItems[1].lower()}'
    if userName not in listOfValidUsers and callingCommand != '$addUser':
      return f'Invalid User - Please add user {listItems[1]}'
    listItems[1] = userName

    if callingCommand in dictValidCommands:
      try:
        return dictValidCommands[callingCommand](listItems)
      except:
        return 'ERROR: Dict Valid Commands failed'
    else:
      return f'Invalid Command {callingCommand}'
  except:
    return 'ERROR'

