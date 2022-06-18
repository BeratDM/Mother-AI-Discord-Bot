from replit import db
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
