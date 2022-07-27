import discord
#import asyncio


async def hiveos_check(d_client, msg):

  #https://discord.com/channels/973611254696542338/973611807178645564/1001515008515125359
  #channel to receive hiveos notifications
  if (msg.channel.id != 973611807178645564):
    return
  
  print("hiveos check is valid")
  value_check_counter = 0
  #dynamic settings feature will be here in the future
  eth_min_value = 40.0
  eth_start = "ethash"
  
  msgcontent = msg.content.split(", ")

  farm_name = msgcontent[0].split(":", 1)[0]
  
  for msgv in msgcontent:
    if msgv.startswith(eth_start):
      xvalue = msgv.split(" ")[1] #ethash 47.41 MH/s
      print(xvalue)
      value_check_counter = value_check_counter + 1
      if float(xvalue) > eth_min_value:
        print("all good")
        #await hiveos_alert(d_client, farm_name, "{0} value is correct".format(eth_start))
      else:
        print("failed")
        await hiveos_alert(d_client, farm_name, "{0} value is NOT correct".format(eth_start))
  if value_check_counter < 1:
    await hiveos_alert(d_client, farm_name, "Unexpected Notification Occurred.")
  
async def hiveos_alert(d_client, farmtext, text1):
  
  #https://discord.com/channels/973611254696542338/1001619777996984433/1001620513229127840
  server = d_client.get_guild(973611254696542338)
  channel = server.get_channel(1001619777996984433)
  msg_obj = await channel.fetch_message(1001620513229127840)
  await channel.send("Hiveos Alert in {0}:\n{1}".format(farmtext, text1))
