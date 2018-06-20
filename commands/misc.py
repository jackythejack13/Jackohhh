import discord
from datetime import datetime

async def ping(client,message):
  timestamp = message.timestamp.microsecond
  newstamp = round((datetime.today().microsecond - timestamp) / 1000,0)
  await client.send_message(message.channel,"PONG! `{}ms`".format(newstamp))
