import discord
from datetime import datetime

async def ping(client,message):
  timestamp = message.timestamp.microsecond
  newstamp = timestamp - datetime.time().microsecond
  await client.send_message(message.channel,"PONG! `{}ms`".format(newstamp))
