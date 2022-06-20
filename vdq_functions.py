from replit import db
import discord
import random 
from random import randrange
from datetime import timedelta

import special

def init_verydeepquotes():
  #fix the list lenght for old inputs
  if "verydeepquotes" in db.keys():
    vdquotes = db["verydeepquotes"]
    for vdq in vdquotes:
      if len(vdq) < 5:
        while(len(vdq) < 5):
          vdq.append(None)
      if vdq[0] == None:
        vdq[0] = ""
      if vdq[1] == None:
        vdq[1] = ""
      if vdq[2] == None:
        vdq[2] = 0
      if vdq[3] == None:
        vdq[3] = ""
      if vdq[4] == None:
        vdq[4] = ""


def update_verydeepquotes(nqtext, msg):

  nqauthor_name = msg.author.name
  nqauthor_id = msg.author.id
  nqdate = str(msg.created_at)
  nqattachmenturl = ""
  if len(msg.attachments) > 0:
    nqattachmenturl = msg.attachments[0].url
  
  newquote = [nqtext, nqauthor_name, nqauthor_id, nqdate, nqattachmenturl]
  if "verydeepquotes" in db.keys():
    vdquotes = db["verydeepquotes"]
    vdquotes.append(newquote)
    db["verydeepquotes"] = vdquotes
  else:
    db["verydeepquotes"] = [newquote]


  if nqtext.startswith("http"):
    response = nqtext + '  \n-{0}'.format(nqauthor_name) + ", {0}".format(str(msg.created_at.year)) + "\n\n" + "Successful. Index: {0}".format(len(db["verydeepquotes"])-1)

  else:
    response = '"' + nqtext + '"  -{0}'.format(nqauthor_name) + ", {0}".format(str(msg.created_at.year)) + "\n\n" + "Successful. Index: {0}".format(len(db["verydeepquotes"])-1)

  
  
  print(response + nqattachmenturl)
  ####
  return(response, nqattachmenturl)

def delete_verydeepquotes(index, messager):
  vdquotes = db["verydeepquotes"]
  if len(vdquotes) > index:
    if vdquotes[index][2] == messager.id or messager.id == special.developer_id:
      quote = vdquotes[index][0]
      quote_attachment = vdquotes[index][4]
      del vdquotes[index]
      db["verydeepquotes"] = vdquotes
      return("'{0}' '{1}' successfully deleted".format(quote, quote_attachment))
    else:
      return("failed to authorize")
  else:
    return("invalid index")

#send a random message from past which has a high probability of being a meme attachment link
async def forbidden_function(msginput):
  print("\n\nStarting Forbidden Function")
  print("Requested by: {0}".format(msginput.author.name))
  start_date = await msginput.channel.history(limit = 5, oldest_first = 1).flatten()
  start_date = start_date[0].created_at
  end_date = await msginput.channel.history(limit = 5, oldest_first = 0).flatten()
  end_date = end_date[0].created_at
  selected_messages = []
  try_count = 0
  print(len(selected_messages))

  
  while (len(selected_messages) < 1 and try_count < 15):
    randd = random_date(start_date, end_date)
    print(randd)
    print("starting the search for a forbidden message. Around: " + str(randd))
    all_messages = await msginput.channel.history(limit=100, around = randd ).flatten()
    for message in all_messages:
      if message.content.startswith("https://cdn.discordapp.com/attachments/"):
        selected_messages.append(message)
      elif len(message.attachments) > 0:
        message.content += " " + message.attachments[0].url
        selected_messages.append(message)
    try_count += 1
    print("updated try count to " + str(try_count))
      
    
  
  if len(selected_messages) > 0:
    print("found {0} forbidden message".format(len(selected_messages)))
    randi = random.choice(range(len(selected_messages)))
    print("selected index: {0}".format(randi))
    chosen_message = selected_messages[randi]
    response = chosen_message.content
    await chosen_message.reply(response, mention_author=False, allowed_mentions = discord.AllowedMentions(
            users=False,         # Whether to ping individual user @mentions
            everyone=False,      # Whether to ping @everyone or @here mentions
            roles=False,         # Whether to ping role @mentions
            replied_user=False))
    
  else:
    response = "Couldn't find a forbidden message"

    await msginput.channel.send(response, allowed_mentions = discord.AllowedMentions(
            users=False,         # Whether to ping individual user @mentions
            everyone=False,      # Whether to ping @everyone or @here mentions
            roles=False,         # Whether to ping role @mentions
            replied_user=False))


def random_date(start, end):
    """
    This function will return a random datetime between two datetime 
    objects.
    """
    delta = end - start
    int_delta = (delta.days * 24 * 60 * 60) + delta.seconds
    random_second = randrange(int_delta)
    return start + timedelta(seconds=random_second)
