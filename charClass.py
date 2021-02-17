import dbHandler
import discord
import random

def onlyLettersFromString(s:str):
	return ''.join(filter(str.isalpha, s))

def formatDict(d, tab=0):
    s = ['{\n']
    for k,v in d.items():
        if isinstance(v, dict):
            v = formatDict(v, tab+1)
        else:
            v = str(v)

        s.append('%s%r: %s,\n' % ('  '*tab, k, v))
    s.append('%s}' % ('  '*tab))
    return ''.join(s)

def embedDescription(content:any) -> str:
	if isinstance(content, dict):
		return formatDict(content)
	else:
		return str(content)


class CharInfo:
	def __init__(self,ctx,name):
		self.name = name
		self.channelID = ctx.channel.id
		self.db = self.dbKeyClass
		self.ctx = ctx

	@classmethod
	async def convert(cls, ctx, argument):
			return cls(ctx,argument)

	@property
	def cleansedName(self):
		alphaLower = onlyLettersFromString(self.name).lower()
		if len(alphaLower) < 3:
			return False, 'TESTINGCHAR'
		else:
			return True, alphaLower

	@property
	def dbKeyClass(self):
		nameValid, lowName = self.cleansedName
		if nameValid:
			return dbHandler.DBkey(f'{str(self.channelID)} {lowName}')
		else:
			return dbHandler.DBkey('TESTINGCHAR')

	def storedVal(self,key,defaultVal):
		try:
			return self.db.data[key]
		except:
			return defaultVal

	def embed(self,description:str = ''):
		color = self.storedVal('color',random.randint(0, 0xffffff))
		imageUrl = self.storedVal('imageUrl',self.ctx.author.avatar_url)
		charEmbed = discord.Embed(color = color)
		charEmbed.set_author(name = self.name)
		charEmbed.set_thumbnail(url = imageUrl)
		charEmbed.description = embedDescription(description)
        # charEmbed.title = "title"
		#charEmbed.description = "description"
		#charEmbed.add_field(name="Field1", value="hi", inline=False)
		#charEmbed.add_field(name="Field2", value=d20.roll(arg), inline=False)
		return charEmbed