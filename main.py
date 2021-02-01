import os
import hypno
import msgParse
import discord
import dbHandler

client = discord.Client(intents=discord.Intents.all())

@client.event
async def on_ready():
  print("Ready!")

@client.event
async def on_message(message):
  ### Don't let the bot run on the messages that it posts
  if message.author == client.user:
    return
  ### All messages are of the form 
  ### $discordBotCommand User Inputs
  if not message.content.startswith('$'):
    return

  listOfUsers = dbHandler.getUsers()
  listOfCommands = ['$addCommand','$getCommand','$rollCommand','$addUser']
  parseContents = msgParse.msgContains(message.content,listOfCommands,listOfUsers, message.guild.id)

  if not isinstance(parseContents, list):
    print(parseContents)
    return

  #$addCommand haven Love-Daddy adv 20
  if parseContents[0] == '$addCommand':
    reply = hypno.addCommand(parseContents)
    await message.channel.send(reply)
    return
  #$getCommand haven
  if parseContents[0] == '$getCommand':
    reply = hypno.currentHypnoAsString(parseContents)
    await message.channel.send(reply)
    return
  #$rollCommand haven 90
  if parseContents[0] == '$rollCommand':
    reply = hypno.callRollHypno(parseContents)
    await message.channel.send(reply)
    return
  if parseContents[0] == '$addUser':
    try:
      reply = dbHandler.addUser(parseContents[1])
    except:
      reply = 'User Added'
    await message.channel.send(reply)
    return


client.run(os.getenv('TOKEN'))
