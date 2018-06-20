import discord
from datetime import datetime

async def ping(client,message):
  timestamp = datetime.fromtimestamp(message.timestamp).microseconds
  await client.send_message(message.channel,"PONG! `{}ms`".format(datetime.time().microseconds))
