import discord
import asyncio
import words
import random



# https://i.imgur.com/3AedjrD.png
async def custom_statusf(client):
  while True:
    try:
      randi = random.choice(range(len(words.custom_status)))
      rand_activity, rand_text, rand_url = words.custom_status[randi]
      if rand_activity == 0:
        await client.change_presence(activity=discord.Game(rand_text))
      elif rand_activity == 1:
        await client.change_presence(activity=discord.Streaming(name=rand_text, url=rand_url))
      elif rand_activity == 2:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=rand_text))
      elif rand_activity == 3:
        await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=rand_text, url=rand_url))
      
    except Exception as e:
      print("failed to set custom status")
      print(e)
    finally:
      await asyncio.sleep(450)
