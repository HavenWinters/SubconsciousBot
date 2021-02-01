from replit import db

def getListOfUsers():
  l = []
  for u in db.keys():
    l.append(u)
  return l


def msgContains(txt:str,listOfValidCommands:list, listOfValidUsers:list):
  """This will be used to add a command"""
  try:
    listItems = txt.split(" ")
    if listItems[0] not in listOfValidCommands:
      # To do. Write a list of valid commands as a help file
      return f'Invalid Command {listItems[0]}'
    if listItems[1] not in listOfValidUsers:
      return f'Invalid User - Please add user {listItems[1]}'
    
    return listItems
  except:
    return "User not valid"
 