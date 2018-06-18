import discord, logging, json, os, sys
from discord.ext import commands

# Define all variables to be used around the script
description = '''Bot description here'''
#bot = commands.Bot(command_prefix='>', description=description)
client = discord.Client()


# Print the starting text
print('---------------')
print('Jackohhh Bot')
print('---------------')
print('Starting Bot...')

@client.event
async def on_message(msg):
	return

@client.event
async def on_ready():
	print('BOT LOADED')
	return

if __name__ == '__main__':
	client.run(os.environ['TOKEN'])
