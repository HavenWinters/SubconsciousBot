import dice
import dbHandler

def addCommandToDB(user:str,command:str,commandProperties:dict):
  userData = dbHandler.getUserInfo(user)
  userData[command.lower()] = commandProperties
  dbHandler.updateUserInfo(user,userData)

 #$addCommand haven Love-Daddy adv 20
def buildAddCommand(user:str,command:str,advantageType:str,total:int):
  return f'{user} {command} {advantageType} {total}'
 #$addCommand haven Love-Daddy adv 20
def addCommand(txt:str):
  """This will be used to add a command"""
  try:
    splitTxt = txt.split(" ")
    user = splitTxt[0]
    command = splitTxt[1]
    advantageType = splitTxt[2]
    total = int(splitTxt[3])
    txt == buildAddCommand(user,command,advantageType,total)
    try:
      addCommandToDB(user.lower(),command.lower(),{"advantageType":advantageType.lower(),"total":total})
      return 'success'
    except:
      return 'failure'
  except:
    return "Invalid. Should be of type User Command AdvantageType Total"

def currentHypnoAsString(user):
  userData = dbHandler.getUserInfo(user)
  s = ''
  for command in userData:
    s = f'{s}\n{command}: {userData[command]["total"]}'
  return s

def callRollHypno(txt:str):
  splitting = txt.lower().split(" ")
  try:
    return rollHypno(splitting[0],int(splitting[1]))
  except:
    return 'Must be of type haven 90'

def rollHypno(user:str, addsUpTo:int):
  '''Increases The users command totals by a rolled amount that cumulativly adds up to the input addsUpTo.'''
  userData = dbHandler.getUserInfo(user)
  randomAddsUpTo = dice.nSidedDie(addsUpTo)
  s = f'Rolls {randomAddsUpTo}\n'
  cumulativeTotal = 0
  rolls = {}
  ### In Order to scale everything appropriately everything is converted to cumulative.
  for command in userData:
    advType = userData[command]['advantageType'].lower()
    roll = dice.rollGivenAdvType(advType,20)
    #s = f'{s}\n{command} rolled {roll} at {advType}'
    cumulativeTotal = cumulativeTotal + roll
    rolls[command] = cumulativeTotal
  if cumulativeTotal <= 0:
    return('Problem with cumulative total')
  ### In order to get the multiplier to be correct it has to be a float however
  ### that will cause problems down the line. 
  ### This is where the cumulative comes intopractice.
  overallScalingFactor = randomAddsUpTo / cumulativeTotal
  prevRoll = 0
  for command in rolls:
    ### Every roll is scaled by the overall scaling factor and then rounded to integer
    scalingRoll = round(rolls[command] * overallScalingFactor)
    ### scaling roll - previous roll is the key to all of this.
    ### because they are both cumulative and scaled and rounded the difference between
    ### them is the actual scaled up roll that takes account of rounding
    ### Example:
    ### assume you wanted the values to add up to 20
    ### assume you rolled 10,5 then the scaling factor was 4/3
    ### you would have 10,15 as your cumulative results
    ### you would then have 13,20 as your cumulative scaled results
    ### finding the differences with the previous values gives you 13,6
    ### 
    ### The rest of the line makes sure that the total is greater than or equal to 0
    ### And makes sure that the new scaled result gets added to the previous total
    userData[command]['total'] = max(0,( userData[command]['total'] + scalingRoll - prevRoll ))
    ### Setting the prevRoll to the current set of rolls after it has been used
    ### Essentially turns this into a lag function where it is looking at the previous roll
    prevRoll = scalingRoll
    s = f'{s}\n{command} :: {userData[command]["total"]}'

  dbHandler.updateUserInfo(user,userData)
  return s
