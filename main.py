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
import msgParse
import messageContains

bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
	print(f'Logged in as {bot.user.name} with id:{bot.user.id}')


@bot.command(pass_context=True, name='test')
async def _test(ctx, arg):
	await ctx.send(arg)


@bot.command(pass_context=True, name='multiarg')
async def _multiarg(ctx, *args):
	await ctx.send('{} arguments: {}'.format(len(args), ', '.join(args)))


@bot.command(pass_context=True, name='add')
async def _add(ctx, a: int, b: int):
	await ctx.send(a + b)


class Sucker(commands.Converter):
	async def convert(self, ctx, argument):
		to_suck = random.choice(ctx.guild.members)
		return '{0.author} sucked {1} because *{2}*'.format(
		    ctx, to_suck, argument)


@bot.command()
async def suck(ctx, *, reason: Sucker):
	await ctx.send(reason)


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
  # do stuff here
  # do not process commands here

  ### Don't let the bot run on the messages that it posts
  if message.author.id == bot.user.id:
    return
  
  if message.content.startswith('$'):
    txt = msgParse.msgToCaller(message)
    if isinstance(txt,str):
      await message.channel.send(txt)
      if not txt.startswith('ERROR'):
        await message.delete()

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
