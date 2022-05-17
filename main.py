import os
import discord
import requests
import json
import random
from replit import db
from datetime import datetime
from keep_alive import keep_alive

client = discord.Client()

developer_id = 275675302494076928



weather_words = ["hava durumu", "weather", "havalar", "bugün hava", "hava", "havada"]

weather_responses1 = ["Today is an overestimated ", "Today will be an exotic ", "Today is going to be a surprising ", "Today is an underestimated ", "Nothing surprising, Today will be "]

weather_responses2 = ["I will continue my efforts at keeping you alive.", "Consider getting into a suitable body wear to expand your life expectancy.", "Don't forget to take the motion tracker.", "I would suspect the outside may offer more danger than you know.", "Remember, they mostly come out at night.. mostly."]

weather_responses3 = ["Have a nice day.", "Stay happy.", "Good luck.", "Session Over.", "Terminating Session..", "Ending.."]

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
  return(text + " -" + author)

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
  ####

  
  #fresponse = update_verydeepquotes(new_vdqtext, message.author.name, message.author.id, str(message.created_at))
        
  #fresponse = fresponse.split("ß")
 # print(fresponse[1] + "------ Index: "+ fresponse[0])
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


  
  if message.content.startswith("mother".casefold() + "."):

    msgrest = message.content.split("mother.".casefold(), 1)
    print(msgrest[1])
    
    if "hello".casefold() in message.content:
      await message.channel.send("Hello!")
      
    if any(word in message.content for word in ["wisdom", "quote"]):
      quote = get_quote2()
      await message.channel.send(quote)

    if db["responding.verydeepquotes"]:
      if "yaz bunu".casefold() in message.content:
        msg_id = message
        if message.reference is not None:
          if message.reference.cached_message is None:
              # Fetching the message
              channel = client.get_channel(message.reference.channel_id)
              msg_id = await channel.fetch_message(message.reference.message_id)
              new_vdqtext = msg_id.content
          else:
              msg_id = message.reference.cached_message
              new_vdqtext = msg_id.content
        else: 
          new_vdqtext = message.content.split('yaz bunu ',)[1]
        #####
        #fresponse = update_verydeepquotes(new_vdqtext, message.author.name, message.author.id, str(message.created_at))
        
        fresponse = update_verydeepquotes(new_vdqtext, msg_id)
        
        await message.channel.send(fresponse,  allowed_mentions = discord.AllowedMentions(
            users=False,         # Whether to ping individual user @mentions
            everyone=False,      # Whether to ping @everyone or @here mentions
            roles=False,         # Whether to ping role @mentions
            replied_user=False))
        return
  
      
      if "özlü söz".casefold() in message.content:
        if "verydeepquotes" in db.keys():
          vdquotes = db["verydeepquotes"]
          randi = random.choice(range(len(vdquotes)))
          vdq = vdquotes[randi]
          vdqtext, vdqauthor_name, vdqdate = vdq[0], vdq[1], vdq[3]
          vdqdate = datetime.strptime(vdqdate, '%Y-%m-%d %H:%M:%S.%f')
          response = vdqtext + " -" + vdqauthor_name + ", " + str(vdqdate.year) + "  ||*Index: {0}*||".format(randi)
          await message.channel.send(response, allowed_mentions = discord.AllowedMentions(
            users=False,         # Whether to ping individual user @mentions
            everyone=False,      # Whether to ping @everyone or @here mentions
            roles=False,         # Whether to ping role @mentions
            replied_user=False))
        return
  
        
      if "sil".casefold() in message.content:
        vdquotes = []
        if "verydeepquotes" in db.keys():
          index = int(message.content.split("sil", 1)[1])
          fresponse = delete_verydeepquotes(index, message.author)
          await message.channel.send(fresponse)
        return


    
    if msgrest[1].startswith("list.özlüsöz"):
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
        
      await message.channel.send(response)  
      



      
  
    if msgrest[1].startswith("responding."):
      r_element = msgrest[1].split("responding.",1)[1]

      if r_element.startswith("özlüsöz "):
        value =r_element.split("özlüsöz ", 1)[1]
        
        if value.lower() == "true":
          db["responding.verydeepquotes"] = True
          await message.channel.send("Özlü Söz Activated.")
        elif value.lower() == "false":
          db["responding.verydeepquotes"] = False
          await message.channel.send("Özlü Söz Deactivated.")
          
  

  
  if any(word in message.content for word in weather_words):
    response = random.choice(weather_responses1) + " 25 C°. " +   random.choice(weather_responses2) + " " + random.choice(weather_responses3)
    await message.channel.send(response)
    return


keep_alive()
client.run(os.environ['TOKEN'])