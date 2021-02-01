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