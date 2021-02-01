### Create a web server and keep pinging it every 30 mins or so
### This keeps the robot alive
from keep_alive import keep_alive
keep_alive()

### The code for the actual Bot
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
      if not txt.startswith('ERROR'):
        await message.delete()



client.run(os.getenv('TOKEN'))
