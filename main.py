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
import d20  # pip install -U d20
import messageContains
import charClass

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
async def delta(ctx, *, char: charClass.CharInfo):
	'''
	!delta Haven
	Brings back the dictionary of information in the character class.
	Used for debugging the class rather than anything in particular.
	'''
	await ctx.send(str(char.__dict__))

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
		await ctx.send(f'{char.name} already exists on channel.')
	else:
		char.db.equals({})
		await ctx.send(f'Hi {char.name}. User Added.')

@bot.command()
async def testEmbed(ctx, char: charClass.CharInfo, *args):
	text = '{} arguments: {}'.format(len(args), ', '.join(args))
	charEmbed = char.embed
	charEmbed.description = text
	await ctx.send(embed=charEmbed)

@bot.command()
async def setImageUrl(ctx, char: charClass.CharInfo, url:str):
	'''
	!setImageUrl Haven https://i.pinimg.com/originals/1e/c6/df/1ec6df3e5d970ec830c5faa320cb602d.jpg

	Sets the image as the new default image for the character.
	It also deletes the message to tidy things up a bit.
	'''
	if char.db.inDB:
		print("updateDB")
		# update DB
		charProperties = char.db.data
		charProperties['imageUrl'] = url
		char.db.equals(charProperties)
		print("updateurl")
		# update URL for embed
		char.imageUrl = url
		print("get embed")
		# get and use embed
		charEmbed = char.embed
		print("get embed1")
		charEmbed.description = 'Image has been successfully updated'
		print("get embed2")
		charEmbed.title = None
		print("get embed3")
		charEmbed.set_image(url=url)
		print("get embed4")
		await ctx.message.delete()
		await ctx.send(embed=charEmbed)
	else:
		await ctx.send(f'Hi {char.name}. User does not exist.')



@bot.command(pass_context=True, name='roll')
async def _roll(ctx, arg: str):
	'''
	!roll 4d6kh3  # highest 3 of 4 6-sided dice
	!roll 2d6ro<3  # roll 2d6s, then reroll any 1s or 2s once
	!roll 8d6mi2  # roll 8d6s, with each die having a minimum roll of 2
	!roll "(1d4 + 1, 3, 2d6kl1)kh1"  # the highest of 1d4+1, 3, and the lower of 2 d6s
	Uses code from https://github.com/avrae/d20
	'''
	embedVar = discord.Embed(color=random.randint(0, 0xffffff))
	embedVar.title = "dice Roll"
	embedVar.set_author(name=ctx.author.display_name,
											icon_url=ctx.author.avatar_url)
	embedVar.description = "Rolling a dice description"
	embedVar.add_field(name="Field1", value="hi", inline=False)
	embedVar.add_field(name="Field2", value=d20.roll(arg), inline=False)

	await ctx.message.delete()
	await ctx.send(embed=embedVar)

	#await ctx.send(d20.roll(arg))


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
