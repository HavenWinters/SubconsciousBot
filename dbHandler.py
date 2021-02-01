from replit import db

def getUsers():
  l = []
  for u in db.keys():
    l.append(u)
  return l

def userExists(user):
  lowcaseUser = user.lower()
  return lowcaseUser in getUsers()

def addUser(user):
  #get current list of users and check that the new one isn't overwriting anything
  lowcaseUser = user.lower()
  if userExists(lowcaseUser):
    return f'ERROR: Unable to overwrite existing user {lowcaseUser}'

  db[lowcaseUser] = {}
  return f'SUCCESS: User {lowcaseUser} added'

def deleteUser(user):
  #get current list of users 
  lowcaseUser = user.lower()
  if not userExists(lowcaseUser):
    return f'ERROR: Unable to delete {lowcaseUser} as they do not exist'

  del db[lowcaseUser]
  return f'SUCCESS: User {lowcaseUser} deleted'

def getUserInfo(user:str):
  lowcaseUser = user.lower()
  if not userExists(lowcaseUser):
    return f'ERROR: Unable to get information from missing user {lowcaseUser}'
  return db[lowcaseUser]

def updateUserInfo(user:str,userInfo:dict):
  lowcaseUser = user.lower()
  if not userExists(lowcaseUser):
    return f'ERROR: Unable to update missing user {lowcaseUser}'
  # Seems that the database keys are immutable and cannot be overwritten
  # Need to delete and then re-add
  del db[lowcaseUser]
  db[lowcaseUser] = userInfo
  return f'SUCCESS: User {lowcaseUser} information updated'

def addCommandToDB(user:str,command:str,commandProperties:dict):
  userData = getUserInfo(user)
  userData[command.lower()] = commandProperties
  updateUserInfo(user,userData)