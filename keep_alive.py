from flask import Flask
from threading import Thread
import time
from subprocess import call
import discord
import asyncio
from datetime import datetime
from os import system

app = Flask('')
#d_client = discord.Client()
@app.route('/')
def home():
  return "Hello, I am alive!"

def run():
  app.run(host = '0.0.0.0', port = 8080)

def keep_alive():
  t = Thread(target = run)
  t.start()

#If you are not on Replit, you probably don't need to use this function
#This function checks the connection to discord and restarts to dodge the 429 TooManyRequests limit
async def keep_discord_connection(d_client):
  await asyncio.sleep(10)
  dc_conn = 0
  dc_conn_last = 1

  server = d_client.get_guild(973611254696542338)
  channel = server.get_channel(988684103257833472)
  msg_obj = await channel.fetch_message(988687689584885820)
  #https://discord.com/channels/973611254696542338/988684103257833472/988687689584885820
  await channel.send("Starting Mother AI")

  
  while True:
    try:
      user = await d_client.fetch_user(d_client.user.id)
      dc_conn = 0
      
    except:  
      now = datetime.now()
      current_time = now.strftime("%D, %H:%M:%S")
      print("Current Time =", current_time)
      print("I CAN'T FETCH MYSELF ;(")

      system("python restarter_2.py")
      with open('restart.sh', 'rb') as file:
        script = file.read()
        #rc = call(script, shell=True)
        rc = call("kill 1", shell=True)
      
      

      dc_conn = 1
    
    finally:
      if dc_conn != dc_conn_last:
        now = datetime.now()
        current_time = now.strftime("%D, %H:%M:%S")
        print("Current Time =", current_time)
        if dc_conn == 1:
          print("I CAN'T FETCH MYSELF ;(")
         
        elif dc_conn == 0:
          print("I can fetch myself :)")
        dc_conn_last = dc_conn
      await asyncio.sleep(30)




def restart_repl(pid):
  now = datetime.now()
  current_time = now.strftime("%D, %H:%M:%S")
  print("Current Time =", current_time)
  print("I CAN'T FETCH MYSELF ;(")
  print("pid: " + str(pid))

  system("python restarter_2.py")

  system("kill {0}".format(pid))
  system("kill 1")
  
  with open('restart.sh', 'rb') as file:
    script = file.read()
    #rc = call(script, shell=True)
    system("kill {0}".format(pid))
    rc = call("kill 1", shell=True)