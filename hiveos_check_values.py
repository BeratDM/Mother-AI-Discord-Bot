import discord
#import asyncio


async def hiveos_check(d_client, msg):

  #https://discord.com/channels/973611254696542338/973611807178645564/1001515008515125359
  #channel to receive hiveos notifications
  if (msg.channel.id != 973611807178645564):
    return
  
  print("hiveos check is valid")

  #dynamic settings feature will be here in the future
  eth_min_value = 40.0
  eth_start = "ethash"
  
  msgcontent = msg.content.split(", ")

  for msgv in msgcontent:
    if msgv.startswith(eth_start):
      xvalue = msgv.split(" ")[1] #ethash 47.41 MH/s
      print(xvalue)
      if float(xvalue) > eth_min_value:
        print("all good")
        await hiveos_alert(d_client, "eth value is correct")
      else:
        print("failed")
        await hiveos_alert(d_client, "eth value is NOT correct")
        

async def hiveos_alert(d_client, text1):
  
  #https://discord.com/channels/973611254696542338/1001619777996984433/1001620513229127840
  server = d_client.get_guild(973611254696542338)
  channel = server.get_channel(1001619777996984433)
  msg_obj = await channel.fetch_message(1001620513229127840)
  await channel.send("Hiveos Alert: {0}".format(text1))
