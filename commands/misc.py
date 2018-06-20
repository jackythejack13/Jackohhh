import discord
from datetime import datetime

async def ping(client,message):
  print(message.timestamp)
  #await client.send_message(message.channel,"PONG! `{}ms`".format(datetime.time().microseconds))
