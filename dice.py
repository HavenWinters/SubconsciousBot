import random
def nSidedDie(n:int):
  """This will be used to roll an nSidedDie"""
  if n > 0:
    return random.randrange(1, n+1)
  elif n == 0:
    return 0
  else:
    return -random.randrange(1, abs(n)+1)

def advNSidedDie(n:int):
  """Creates 2 dice with n sides and returns the highest"""
  return max(nSidedDie(n),nSidedDie(n))

def disNSidedDie(n:int):
  """Creates 2 dice with n sides and returns the smallest"""
  return min(nSidedDie(n),nSidedDie(n))

def rollGivenAdvType(advType:str,n:int):
  if advType.lower() == 'adv':
    return advNSidedDie(n)
  elif advType.lower() == 'dis':
    return disNSidedDie(n)
  else:
    return nSidedDie(n)


def modifyCommandTotals(userData, addsUpTo:int):
  '''Increases The users command totals by a rolled amount that cumulativly adds up to the input addsUpTo.'''
  cumulativeTotal = 0
  rolls = {}
  ### In Order to scale everything appropriately everything is converted to cumulative.
  for command in userData:
    advType = userData[command]['advantageType'].lower()
    roll = rollGivenAdvType(advType,20)
    cumulativeTotal = cumulativeTotal + roll
    rolls[command] = cumulativeTotal
  if cumulativeTotal <= 0:
    print('ERROR: Problem with cumulative total')
    return userData
  ### In order to get the multiplier to be correct it has to be a float however
  ### that will cause problems down the line. 
  ### This is where the cumulative comes intopractice.
  overallScalingFactor = addsUpTo / cumulativeTotal
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
    ### finding the differences with the previous values gives you 13,7
    ### 
    ### The rest of the line makes sure that the total is greater than or equal to 0
    ### And makes sure that the new scaled result gets added to the previous total
    userData[command]['total'] = max(0,( userData[command]['total'] + scalingRoll - prevRoll ))
    ### Setting the prevRoll to the current set of rolls after it has been used
    ### Essentially turns this into a lag function where it is looking at the previous roll
    prevRoll = scalingRoll
  return userData


def rollXNSidedDice(x:int, n:int):
 """This will be used to roll X nSidedDice"""
 if x > 0:
   results = []
   count = 0
   while count < x:
     results.append(nSidedDie(n))
     count += 1
   return results
 else:
   return "Error: X need to be greater than 0"
