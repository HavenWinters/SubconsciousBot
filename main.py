### Create a web server and keep pinging it every 30 mins or so
### This keeps the robot alive
from keep_alive import keep_alive
keep_alive()

###https://stackoverflow.com/questions/50662953/command-parsing-for-discord-py
### The code for the actual Bot
import os
import random
import discord
from discord.ext import commands
import messageContains
import charClass
import commands as cmds

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
	print(f'Logged in as {bot.user.name} with id:{bot.user.id}')

### Testing Function
@bot.command(pass_context=True, name='test')
async def _test(ctx, arg):
	await ctx.send(arg)

### Testing Function
@bot.command(pass_context=True, name='multiarg')
async def _multiarg(ctx, *args):
	await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))

### Testing Function
@bot.command(pass_context=True, name='add')
async def _add(ctx, a: int, b: int):
	await ctx.send(a + b)


@bot.command()
async def addChar(ctx, *, char: charClass.CharInfo):
	'''
	!addChar Haven
	Adds a character called Haven to the database.
	Provided of course that it does not already exist.
	Characters in the database are discord channel dependant.
	So you can have a Haven character in multiple RPs.
	'''
	if char.db.inDB:
		charEmbed = char.embed(f'{char.name} already exists on channel.')
	else:
		char.db.data = {}
		charEmbed = char.embed(f'{char.name} Added.')

	charEmbed.title = f'Adding {char.name}'
	await ctx.send(embed=charEmbed)

@bot.command()
async def dbInfo(ctx, char: charClass.CharInfo, *args):
	'''
	!dbInfo Haven
	Brings back the dictionary of information in the character class.
	Used for debugging the class rather than anything in particular.
	'''
	charEmbed = char.embed(char.__dict__)
	await ctx.send(embed=charEmbed)

@bot.command()
async def setImageUrl(ctx, char: charClass.CharInfo, url:str):
	'''
	!setImageUrl Haven https://i.pinimg.com/originals/1e/c6/df/1ec6df3e5d970ec830c5faa320cb602d.jpg

	Sets the image as the new default image for the character.
	It also deletes the message to tidy things up a bit.
	'''
	if char.db.inDB:
		updateSuccess, updateResult = char.db.updateSubKey('imageUrl',url)
		if updateSuccess:
			await ctx.message.delete()

		# get and use embed
		charEmbed = char.embed(updateResult)
		charEmbed.title = 'Set Image URL'
		await ctx.send(embed=charEmbed)
	else:
		await ctx.send(f'Hi {char.name}. User does not exist.')



@bot.command()
async def getCommands(ctx, *, char: charClass.CharInfo):
	'''
	!getCommands Haven
	Checks the Haven character for any commands and prints them to discord
	'''
	if char.db.inDB:
		d = char.db.data
		commandDict = d.get('commands',{})
		gc = cmds.GroupedCommands(commandDict)
		s = ''
		for c in gc.commandList:
			s = f'{s}\n{c.name} :: {c.intensity}'
		charEmbed = char.embed('No commands' if s == '' else s)
		charEmbed.title = 'Commands'
		await ctx.send(embed=charEmbed)
	else:
		await ctx.send('Character not yet added')

@bot.command()
async def addCommand(ctx, char: charClass.CharInfo,name:str, advType:int = 0, intensity:int = 0):
	'''
	!getCommands Haven
	Checks the Haven character for any commands and prints them to discord
	'''
	if char.db.inDB:
		d = char.db.data
		commandDict = d.get('commands',{})
		gc = cmds.GroupedCommands(commandDict)
		gc.addCommand(cmds.Command(name,advType,intensity))
		d['commands'] = gc.output
		char.db.data = d
		charEmbed = char.embed(f'Added {name}')
		charEmbed.title = 'Adding Command'
		await ctx.send(embed=charEmbed)
	else:
		await ctx.send('Character not yet added')

@bot.command()
async def deleteCommand(ctx, char: charClass.CharInfo,name:str):
	'''
	!getCommands Haven
	Checks the Haven character for any commands and prints them to discord
	'''
	if char.db.inDB:
		d = char.db.data
		commandDict = d.get('commands',{})
		gc = cmds.GroupedCommands(commandDict)
		gc.deleteCommand(name)
		d['commands'] = gc.output
		char.db.data = d
		charEmbed = char.embed(f'Deleted {name}')
		charEmbed.title = 'Deleting Command'
		await ctx.send(embed=charEmbed)
	else:
		await ctx.send('Character not yet added')




#https://discordpy.readthedocs.io/en/latest/faq.html#why-does-on-message-make-my-commands-stop-working
@bot.listen('on_message')
async def parseMessage(message):
	'''
	Every discord message gets routed through here.
	It does not run on messages that the bot writes due to some extra code.
	It is used for parsing for phrases inside of the text.
	Currently looking for specific phrases within speech marks.
	Doesn't process ! commands
	'''

	### Don't let the bot run on the messages that it posts
	if message.author.id == bot.user.id:
		return
	
	hypSlut = messageContains.markSpokenPhrase(message.content,'hypno slut',100)
	downGirl = messageContains.markSpokenPhrase(message.content,'down girl',100)
	if hypSlut != '' or downGirl != '':
		 await message.channel.send(f'{hypSlut}\n\n{downGirl}')



@bot.event
async def on_command_error(ctx, error):
	if isinstance(error, commands.MissingRequiredArgument):
		await ctx.send("Missing required argument: {}".format(error.param))
	elif isinstance(error, commands.BadArgument):
		await ctx.send("Could not parse commands argument.")


bot.run(os.getenv('TOKEN'))
