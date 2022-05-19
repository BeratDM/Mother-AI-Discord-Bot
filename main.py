import os
import discord
import requests
import json
import random
import re
from replit import db
from datetime import datetime
from keep_alive import keep_alive
import words

client = discord.Client()

developer_id = 275675302494076928


if "responding.verydeepquotes" not in db.keys():
  db["responding.verydeepquotes"] = True

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

def update_verydeepquotes(nqtext, msg):

  nqauthor_name = msg.author.name
  nqauthor_id = msg.author.id
  nqdate = str(msg.created_at)
  
  newquote = [nqtext, nqauthor_name, nqauthor_id, nqdate]
  if "verydeepquotes" in db.keys():
    vdquotes = db["verydeepquotes"]
    vdquotes.append(newquote)
    db["verydeepquotes"] = vdquotes
  else:
    db["verydeepquotes"] = [newquote]
  
  response = '"' + nqtext + '"  -{0}'.format(nqauthor_name) + ", {0}".format(str(msg.created_at.year)) + "\n\n" + "Successful. Index: {0}".format(len(db["verydeepquotes"])-1)
  print(response)
  ####
  return(response)

def delete_verydeepquotes(index, messager):
  vdquotes = db["verydeepquotes"]
  if len(vdquotes) > index:
    if vdquotes[index][2] == messager.id or messager.id == developer_id:
      quote = vdquotes[index][0]
      del vdquotes[index]
      db["verydeepquotes"] = vdquotes
      return("'{0}' successfully deleted".format(quote))
    else:
      return("failed to authorize")
  else:
    return("invalid index")


@client.event
async def on_ready():
  print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
  if message.author == client.user:
    return


  
  if message.content.casefold().startswith("mother."):

    msgrest = message.content.split(".", 1)[1]
    print(message.author.name + ": " + msgrest)
    
    if any(word in message.content.casefold() for word in ["hello", "hi", "hey", "wasup"]):
      await message.channel.send(random.choice(words.greeting_response1))
    
    if msgrest.startswith(("list.özlüsöz", "list.vdq")):
      vdquotes = ["","",0,""]
      response = ""
      if "verydeepquotes" in db.keys():
        vdquotes = db["verydeepquotes"]

      index = 0  
      for vdq in vdquotes:
        vdqtext, vdqauthor_name, vdqdate = vdq[0], vdq[1], vdq[3]
        vdqdate = datetime.strptime(vdqdate, '%Y-%m-%d %H:%M:%S.%f')
        response = response + " ||Index: {0}||".format(index) + '     "{0}"'.format(vdqtext) + "  - {0}, ".format(vdqauthor_name) + '{0}'.format(str(vdqdate.year) +  '\n\n')
        index += 1
        
      await message.channel.send(response, allowed_mentions = discord.AllowedMentions(
            users=False,         # Whether to ping individual user @mentions
            everyone=False,      # Whether to ping @everyone or @here mentions
            roles=False,         # Whether to ping role @mentions
            replied_user=False))  
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
        elif msgrest.casefold().startswith("yaz bunu "):
          try:
            msglink = re.split("yaz bunu ", msgrest, flags=re.IGNORECASE)[1]
          except:
            pass
          #'https://discordapp.com/channels/guild_id/channel_id/message_id'
        link = msglink.split("/")
          
        server_id = int(link[4])
        channel_id = int(link[5])
        msg_id = int(link[6])
        
        try:
          server = client.get_guild(server_id)
          channel = server.get_channel(channel_id)
          msg_obj = await channel.fetch_message(msg_id)
          new_vdqtext = msg_obj.content
          
        except AttributeError:
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
        
        fresponse = update_verydeepquotes(new_vdqtext, msg_obj)
        
        await message.channel.send(fresponse,  allowed_mentions = discord.AllowedMentions(
            users=False,         # Whether to ping individual user @mentions
            everyone=False,      # Whether to ping @everyone or @here mentions
            roles=False,         # Whether to ping role @mentions
            replied_user=False))
        return
  
      if any(word in message.content.casefold() for word in ("özlü söz", "vdq", "very deep", "deep quote", "deep wisdom")):
        if "verydeepquotes" in db.keys():
          vdquotes = db["verydeepquotes"]
          randi = random.choice(range(len(vdquotes)))
          vdq = vdquotes[randi]
          vdqtext, vdqauthor_name, vdqdate = vdq[0], vdq[1], vdq[3]
          vdqdate = datetime.strptime(vdqdate, '%Y-%m-%d %H:%M:%S.%f')
          response = '"{0}"'.format(vdqtext) + " -" + vdqauthor_name + ", " + str(vdqdate.year) + "  ||*Index: {0}*||".format(randi)
          print(response)
          await message.channel.send(response, allowed_mentions = discord.AllowedMentions(
            users=False,         # Whether to ping individual user @mentions
            everyone=False,      # Whether to ping @everyone or @here mentions
            roles=False,         # Whether to ping role @mentions
            replied_user=False))
        return
  
        
      
      
      if msgrest.casefold().startswith(("sil", " sil", "del", " del", "delete", " delete")):
        vdquotes = []
        if "verydeepquotes" in db.keys():
          index = message.content.casefold().split()
          try:
            index = int(index[1])
          except:
            index = int(index[len(index)-1])
          fresponse = delete_verydeepquotes(index, message.author)
          print(fresponse)
          await message.channel.send(fresponse, allowed_mentions = discord.AllowedMentions(
            users=False,         # Whether to ping individual user @mentions
            everyone=False,      # Whether to ping @everyone or @here mentions
            roles=False,         # Whether to ping role @mentions
            replied_user=False))
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

    
    
keep_alive()
client.run(os.environ['TOKEN'])
