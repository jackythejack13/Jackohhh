import discord
from datetime import datetime

async def ping(client,message):
  timestamp = message.timestamp.microsecond
  newstamp = datetime.today().microsecond - timestamp
  await client.send_message(message.channel,"PONG! `{}ms`".format(newstamp))
