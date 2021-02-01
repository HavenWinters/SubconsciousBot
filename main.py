import os
### Need to do pip install to get this thing up and running at the moment which is very
### annoying. That is done in the shell.
### This is probably not the best way of doing all of this to be honest.
### also the discord-py-slash-command stuff is still being worked on and might break
### at any moment.
import dice
print(dice.advNSidedDie(20))
import hypno

#pip install -U discord-py-slash-command
#import discord-py-slash-command

import discord
#from discord_slash import SlashCommand # Importing the newly installed library.
#from discord_slash.utils import manage_commands # Allows us to manage the command settings.

# replits db
from replit import db
#for k in db.keys():
#  del db[k]
import random

#guild_ids = [805479597822836777]
client = discord.Client(intents=discord.Intents.all())

#slash = SlashCommand(client, auto_register=True) # Declares slash commands through the client.


# function to update the db through discord
def insert_db(insert_message):
	if "db_txt" in db.keys():
		db_txt = db["db_txt"]
		db_txt.append(insert_message)
		db["db_txt"] = db_txt
	else:
		db["db_txt"] = [insert_message]


# delete function to delete entries in db by index
def delete_db(index):
	db_txt = db["db_txt"]
	if len(db_txt) > index:
		del db_txt[index]
		db["db_txt"] = db_txt


@client.event
async def on_ready():
	print("Ready!")


# my test junk
@client.event
async def on_message(message):

	#msg = message.content

	options = []
	# if db is not empty
	if "db_txt" in db.keys():
		#await message.channel.send("true")
		options = options + db["db_txt"]

	if message.author == client.user:
		return

	if message.content.startswith('$hi'):
		await message.channel.send("hello")
		return

	#$addCommand haven Love-Daddy adv 20
	if message.content.startswith('$addCommand'):
		reply = hypno.addCommand(message.content.split(" ", 1)[1])
		await message.channel.send(reply)
		return
	#$getCommand haven
	if message.content.startswith('$getCommand'):
		reply = hypno.currentHypnoAsString(message.content.split(" ", 1)[1])
		await message.channel.send(reply)
		return
  #$rollCommand haven
	if message.content.startswith('$rollCommand'):
		reply = hypno.callRollHypno(message.content.split(" ", 1)[1])
		await message.channel.send(reply)
		return

	if message.content.startswith("$insert"):
		#splits the msg into an array size 2 and we grab the second element
		insert_txt = message.content.split("$insert ", 1)[1]
		insert_db(insert_txt)
		await message.channel.send("New entry added")

	if message.content.startswith("$delete"):
		db_txt = []
		# if db is not empty
		if "db_txt" in db.keys():
			#splits the msg into an array size 2 and we grab the second element
			delete_index = int(message.content.split("$delete ", 1)[1])
			delete_db(delete_index)
			await message.channel.send("Entry was deleted")
		await message.channel.send(db_txt)

	if message.content.startswith("$list"):
		db_txt = []
		# if db is not empty
		if "db_txt" in db.keys():
			db_txt = db["db_txt"]
		await message.channel.send(db_txt)

	if message.content.startswith("$length"):
		#await message.channel.send("I made it here")
		db_txt = []
		# if db is not empty
		if "db_txt" in db.keys():
			db_txt = db["db_txt"]
		await message.channel.send(len(db_txt))

	if message.content.startswith("$getran"):
		await message.channel.send(random.choice(options))


#end of my junk

#@slash.slash(
#  name="test",
#  description="this should do something. anything.",
#  options=[manage_commands.create_option(
#    name = "argone",
#    description = "description of first argument",
#    option_type = 3,
#    required = True
#  )],
#  guild_ids=guild_ids
#)
#async def _test(ctx, argone: str):
#await ctx.channel.send(content=f"You responded with {argone}.")
#    await ctx.send(content=f"You responded with {argone}.")

client.run(os.getenv('TOKEN'))
