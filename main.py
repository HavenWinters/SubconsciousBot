import os
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
  if message.content.startswith('$'):
    txt = msgParse.msgToCaller(message)
    if isinstance(txt,str):
      await message.channel.send(txt)
      return
    return


client.run(os.getenv('TOKEN'))
