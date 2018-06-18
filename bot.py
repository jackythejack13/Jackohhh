import discord, logging, json, os, sys
from discord.ext import commands

# Define all variables to be used around the script
description = '''Bot description here'''
#bot = commands.Bot(command_prefix='>', description=description)
client = discord.Client()

errorChannel = 'unset'

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
	for server in client.servers:
		if server.id == '327604485386010636':
			for channel in server.channels:
				if channel.id == '455617398465363970':
					errorChannel = channel
					break
			break
	print('BOT LOADED')
	print('Error logging channel: {}'.format(errorChannel.name))
	await client.change_presence(game=discord.Game(name='Spotify',type=2),status=discord.Status.dnd)
	await client.send_message(errorChannel,'I TOO HAVE BEEN REBORN!!!!!!')
	return

if __name__ == '__main__':
	client.run(os.environ['TOKEN'])
