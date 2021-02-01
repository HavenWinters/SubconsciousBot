def msgContains(txt:str,listOfValidCommands:list, listOfValidUsers:list, serverID: int):
  """This will be used to add a command"""
  try:
    listItems = txt.split(" ")
    if listItems[0] not in listOfValidCommands:
      # To do. Write a list of valid commands as a help file
      return f'Invalid Command {listItems[0]}'
    listItems[1] = f'{serverID} {listItems[1].lower()}'
    if listItems[1] not in listOfValidUsers and listItems[0] != '$addUser':
      return f'Invalid User - Please add user {listItems[1].split(" ")[1]}'
    return listItems
  except:
    return "User not valid"
 