import dbHandler

def onlyLettersFromString(s:str):
  return ''.join(filter(str.isalpha, s))


class CharInfo:
  def __init__(self,ctx,name):
    self.name = name
    self.channelID = ctx.channel.id
    self.db = self.dbKeyClass

  @classmethod
  async def convert(cls, ctx, argument):
      return cls(ctx,argument)

  def cleansedName(self):
    alphaLower = onlyLettersFromString(self.name).lower()
    if len(alphaLower) < 3:
      return False, 'TESTINGCHAR'
    else:
      return True, alphaLower

  @property
  def dbKeyClass(self):
    nameValid, lowName = self.cleansedName()
    if nameValid:
      return dbHandler.DB(f'{str(self.channelID)} {lowName}')
    else:
      return dbHandler.DB('TESTINGCHAR')