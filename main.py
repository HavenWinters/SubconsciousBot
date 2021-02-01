import os
import hypno
import msgParse
import discord

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

  listOfUsers = msgParse.getListOfUsers()
  listOfCommands = ['$addCommand','$getCommand','$rollCommand']
  parseContents = msgParse.msgContains(message.content,listOfCommands,listOfUsers)

  if not isinstance(parseContents, list):
    print(parseContents)
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
  #$rollCommand haven 90
  if message.content.startswith('$rollCommand'):
    reply = hypno.callRollHypno(message.content.split(" ", 1)[1])
    await message.channel.send(reply)
    return


client.run(os.getenv('TOKEN'))
