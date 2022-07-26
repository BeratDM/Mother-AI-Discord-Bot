import os
import discord
import requests
import json
import random
import re
from replit import db
from datetime import datetime
import keep_alive as ka
import words, special
import vdq_functions as vdq_f
from hiveos_check_values import hiveos_check
import time
import asyncio
import threading
#from discord.ui import Button, View

client = discord.Client(intents=discord.Intents.default())

no_mentions = discord.AllowedMentions(
            users=False,         # Whether to ping individual user @mentions
            everyone=False,      # Whether to ping @everyone or @here mentions
            roles=False,         # Whether to ping role @mentions
            replied_user=False)

vdq_f.init_verydeepquotes()

if "responding.verydeepquotes" not in db.keys():
  db["responding.verydeepquotes"] = True

if "forbidden.settings" not in db.keys():
  db["forbidden.settings"] = [True, True, True]

def get_quote1():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]["q"] + " -" + json_data[0]["a"]
  return(quote)

def get_quote2():
  
  response = requests.get("https://type.fit/api/quotes")
  json_data = json.loads(response.text)
  aquote = random.choice(list(json_data))
  text, author = aquote["text"], aquote["author"]
  return(text + " -" + author + "\n")

async def forbidden_settings(client, message, msgrest_1):
        if msgrest_1.startswith(".links"):
          msgrest_1 = msgrest_1.split()[1]
          if msgrest_1 == "0":
            db["forbidden.settings"][0] = True
            await message.channel.send("forbidden links enabled.")
          elif msgrest_1 == "1":
            db["forbidden.settings"][0] = False
            await message.channel.send("forbidden links disabled.")
        if msgrest_1.startswith(".attachments"):
          msgrest_1 = msgrest_1.split()[1]
          if msgrest_1 == "0":
            db["forbidden.settings"][1] = True
            await message.channel.send("forbidden attachments enabled.")
          elif msgrest_1 == "1":
            db["forbidden.settings"][1] = False
            await message.channel.send("forbidden attachments disabled.")
        if msgrest_1.startswith(".youtube"):
          msgrest_1 = msgrest_1.split()[1]
          if msgrest_1 == "0":
            db["forbidden.settings"][2] = True
            await message.channel.send("Youtube links enabled.")
          elif msgrest_1 == "1":
            db["forbidden.settings"][2] = False
            await message.channel.send("Youtube links disabled.")
        if msgrest_1.startswith(".imgur"):
          msgrest_1 = msgrest_1.split()[1]
          if msgrest_1 == "0":
            db["forbidden.settings"][3] = True
            await message.channel.send("imgur links enabled.")
          elif msgrest_1 == "1":
            db["forbidden.settings"][3] = False
            await message.channel.send("imgur links disabled.")
        if msgrest_1 == "":

          response = "Here Are The Forbidden Function Settings\n"
          response += "\nlinks: " + str(db["forbidden.settings"][0])
          response += "\nattachments: " + str(db["forbidden.settings"][1])
          response += "\nyoutube: " + str(db["forbidden.settings"][2])
          response += "\nimgur: " + str(db["forbidden.settings"][3])
          response += "\n\n Example usage: Mother.forbidden.settings.attachments 1"

          #settings_view = View()
          #links_button = Button("Links")
          #if db["forbidden.settings"][0]:
          #  links_button.label = "Links: ON"
          #  links_button.style = ButtonStyle.green
          #else:
          #  links_button.label = "Links: OFF"
          #  links_button.style = ButtonStyle.grey
          #settings_view.add_item(links_button)

          
          await message.channel.send(response)

@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))
  #ka.d_client = client
  asyncio.create_task(ka.keep_discord_connection(client))
  

####################
  #On Message#
####################

@client.event
async def on_message(message):
  if message.author == client.user:
    return
  await hiveos_check(client, message)
  

  if message.content.casefold().startswith("mother."):

    print(str(message.guild) + " -- " + str(message.channel))
    
    msgrest = message.content.split(".", 1)[1]
    print(message.author.name + ": " + msgrest)
    
    if any(word in message.content.casefold() for word in ["hello", "hi", "hey", "wasup"]):
      await message.channel.send(random.choice(words.greeting_response1))

    if msgrest.startswith("forbidden"):
      msgrest_1 = msgrest.split("forbidden", 1)[1]
      if msgrest_1.startswith(".settings"):
        try:
          msgrest_1 = msgrest_1.split(".settings", 1)[1]
        except:
          msgrest_1 = ""
        await forbidden_settings(client, message, msgrest_1)
      else:
        await vdq_f.forbidden_function(message, client)
    
    if msgrest.startswith(("list.özlüsöz", "list.vdq")):
      vdquotes = ["","",0,"",""]
      response = ""
      if "verydeepquotes" in db.keys():
        vdquotes = db["verydeepquotes"]

      index = 0  
      for vdq in vdquotes:
        vdqtext, vdqauthor_name, vdqdate, vdqattachment = vdq[0], vdq[1], vdq[3], vdq[4]
        vdqdate = datetime.strptime(vdqdate, '%Y-%m-%d %H:%M:%S.%f')
        response = response + " ||Index: {0}||".format(index) + '     "{0}"'.format(vdqtext) + " {1}  - {0}, ".format(vdqauthor_name, vdqattachment) + '{0}'.format(str(vdqdate.year) +  '\n\n')
        index += 1
        
      await message.channel.send(response, allowed_mentions = no_mentions)
      return

    if db["responding.verydeepquotes"]:
      
      if "yaz bunu" in message.content.casefold() or msgrest.startswith(("newvdq ", " newvdq ")):
        msg_obj = message
        msglink = "https://discordapp.com/channels/0/0/0"
        if msgrest.startswith("newvdq "):
          try:
            msglink = msgrest.split("newvdq ")[1]
          except:
            pass
        elif msgrest.casefold().startswith(("yaz bunu ", " yaz bunu")):
          try:
            msglink = re.split("yaz bunu ", msgrest, flags=re.IGNORECASE)[1]
          except:
            pass
          #'https://discordapp.com/channels/guild_id/channel_id/message_id'
        link = msglink.split("/")

        
        try:  
          
          server_id = int(link[4])
          channel_id = int(link[5])
          msg_id = int(link[6])
        
          server = client.get_guild(server_id)
          channel = server.get_channel(channel_id)
          msg_obj = await channel.fetch_message(msg_id)
          new_vdqtext = msg_obj.content
          
        except: # AttributeError:
          #link not found
          
          if message.reference is not None:
            if message.reference.cached_message is None:
                # Fetching the message
                channel = client.get_channel(message.reference.channel_id)
                msg_obj = await channel.fetch_message(message.reference.message_id)
                new_vdqtext = msg_obj.content
            else:
                msg_obj = message.reference.cached_message
                new_vdqtext = msg_obj.content
          else: 
            new_vdqtext = re.split('yaz bunu ', message.content, flags=re.IGNORECASE)[1]
        
        fresponse, fresponse_attachmenturl = vdq_f.update_verydeepquotes(new_vdqtext, msg_obj)

        if fresponse_attachmenturl != "":
         await message.channel.send(fresponse_attachmenturl, allowed_mentions = no_mentions)
        
        await message.channel.send(fresponse,  allowed_mentions = no_mentions)
        
        return
  
      if any(word in message.content.casefold() for word in ("özlü söz", "vdq", "very deep", "deep quote", "deep wisdom", "laf", "özlüsöz")):
        if "verydeepquotes" in db.keys():
          vdquotes = db["verydeepquotes"]
          randi = random.choice(range(len(vdquotes)))
          for wrd in msgrest.split():
            if wrd.isdigit():
              randi = int(wrd)
          if randi > len(vdquotes) - 1:
            response = "I could not find the index you wanted."
            await message.channel.send(response, allowed_mentions = no_mentions)
            return 
          vdq = vdquotes[randi]
          vdqtext, vdqauthor_name, vdqdate, vdqattachment = vdq[0], vdq[1], vdq[3], vdq[4]
          vdqdate = datetime.strptime(vdqdate, '%Y-%m-%d %H:%M:%S.%f')
          response = '"{0}"'.format(vdqtext) + " -" + vdqauthor_name + ", " + str(vdqdate.year) + "  ||*Index: {0}*||".format(randi)
          print(response)

          if vdqattachment == "":
            response = vdqattachment 
            
          await message.channel.send(response, allowed_mentions = no_mentions)
        return
  
        
      
      
      if msgrest.casefold().startswith(("sil", " sil", "del", " del", "delete", " delete")):
        vdquotes = []
        if "verydeepquotes" in db.keys():
          index = message.content.casefold().split()
          try:
            index = int(index[1])
          except:
            index = int(index[len(index)-1])
          fresponse = vdq_f.delete_verydeepquotes(index, message.author)
          print(fresponse)
          await message.channel.send(fresponse, allowed_mentions = no_mentions)
        return


    

  
    if msgrest.startswith("responding."):
      r_element = msgrest.split("responding.",1)[1]

      if r_element.startswith(("özlüsöz ", "vdq ")):
        value =r_element.split()[1] #("özlüsöz ", "vdq ")
        if value.lower() == "true":
          db["responding.verydeepquotes"] = True
          await message.channel.send("Activated. Very Deep Quotes")
        elif value.lower() == "false":
          db["responding.verydeepquotes"] = False
          await message.channel.send("Deactivated. Very Deep Quotes")
      
      return
          
  
    if any(word in message.content.casefold() for word in ["wisdom", "quote"]):
      quote = get_quote2()
      await message.channel.send(quote)
      return
    
    if any(word in message.content.casefold() for word in ("Thanks", "thank you", "appreciated", "thx", "thank")):
      response = random.choice(words.glad_response1)
      await message.channel.send(response)
      
  if any(word in message.content for word in words.weather_words):
    response = random.choice(words.weather_responses1) + " 25 C°. " +   random.choice(words.weather_responses2) + " " + random.choice(words.weather_responses3)
    await message.channel.send(response)
    return


  
    

ka.keep_alive()
client.run(os.environ['TOKEN'])
