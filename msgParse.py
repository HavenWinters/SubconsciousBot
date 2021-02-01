import dice
import dbHandler

def prettyPrint(commands):
  s = ''
  for command in commands:
    s = f'{s}\n{command}:: {commands[command]["total"]}'
  return s

def msgToCaller(msg):
  """This will be used to add a command"""
  listOfValidUsers = dbHandler.getUsers()
  dictValidCommands = {}
  dictValidCommands['$addCommand'] = callAddCommand
  dictValidCommands['$getCommand'] = callGetCommand
  dictValidCommands['$rollCommand'] = callRollCommand
  dictValidCommands['$addUser'] = dbHandler.addUser

  try:
    ## split the text up into parts
    listItems = msg.content.split(" ")
    callingCommand = listItems[0]
    userName = f'{msg.guild.id} {listItems[1].lower()}'
    if userName not in listOfValidUsers and callingCommand != '$addUser':
      return f'ERROR: Invalid User - Please add user {listItems[1]}'
    listItems[1] = userName

    if callingCommand in dictValidCommands:
      try:
        return dictValidCommands[callingCommand](listItems)
      except:
        return 'ERROR: Dict Valid Commands failed'
    else:
      return f'ERROR: Invalid Command {callingCommand}'
  except:
    return 'ERROR: Unknown Error'

 #$addCommand haven Love-Daddy adv 20
def callAddCommand(parseInputs:list):
  """This will be used to add a command"""
  errMsg = "ERROR: Should be of type User Command AdvantageType ['adv','dis','nat'] Total"
  try:
    user = parseInputs[1]
    command = parseInputs[2]
    advantageType = parseInputs[3]
    total = int(parseInputs[4])
    if advantageType in ['adv','dis','nat'] and total >= 0:
      dbHandler.addCommandToDB(user,command.lower(),{"advantageType":advantageType.lower(),"total":total})
      return f'Added Command {command}'
    return errMsg
  except:
    return errMsg


#getCommand haven
def callGetCommand(parseInputs:list):
  userData = dbHandler.getUserInfo(parseInputs[1])
  return prettyPrint(userData)

#rollCommand haven 90
def callRollCommand(parseInputs:list):
  userName = parseInputs[1]
  addsUpTo = int(parseInputs[2])
  userData = dbHandler.getUserInfo(userName)
  randomAddsUpTo = dice.nSidedDie(addsUpTo)
  modifyTotals = dice.modifyCommandTotals(userData,randomAddsUpTo)
  dbHandler.updateUserInfo(userName,modifyTotals)
  return f'Rolled {randomAddsUpTo} out of {addsUpTo}\n{prettyPrint(modifyTotals)}'