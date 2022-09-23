import discord
import asyncio
import words
import random
import special as sp

status_choice = -1


async def custom_status_check(client, message, msgrest_1):
    global status_choice
    if (msgrest_1.startswith(".set")
            and (message.author.id == sp.developer_id)):
        msgrest_1 = msgrest_1.split()[1]
        if int(msgrest_1) >= 0:
            if int(msgrest_1) < len(words.custom_status):
                status_choice = int(msgrest_1)
                await custom_statusf(client)
                await message.channel.send(
                    "Custom status is set to {0}".format(status_choice))
                # 2nd await doesn't work
            else:
                await message.channel.send(
                    "Custom status index is out of range")
        elif msgrest_1 == "-1":
            status_choice = -1
            await custom_statusf(client)
            await message.channel.send("Custom status is now random")
            # 2nd await doesn't work
        else:
            await message.channel.send("Custom status choice is invalid")

    if msgrest_1 == "":

        response = "Here Are The Custom Status Settings\n"
        response += "\nset: set custom status by indicating the index, -1 for random status."
        response += "\n\n Example usage: Mother.customstatus.set -1"

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


# https://i.imgur.com/3AedjrD.png
async def custom_statusf(client):
    while True:
        try:
            if status_choice <= -1:
                randi = random.choice(range(len(words.custom_status)))
            else:
                randi = status_choice
            try:
                rand_activity, rand_text, rand_url = words.custom_status[randi]
            except IndexError:
                print("custom status choice is out of range")
                randi = random.choice(range(len(words.custom_status)))
                rand_activity, rand_text, rand_url = words.custom_status[randi]
            if rand_activity == 0:
                await client.change_presence(activity=discord.Game(rand_text))
            elif rand_activity == 1:
                await client.change_presence(
                    activity=discord.Streaming(name=rand_text, url=rand_url))
            elif rand_activity == 2:
                await client.change_presence(activity=discord.Activity(
                    type=discord.ActivityType.watching, name=rand_text))
            elif rand_activity == 3:
                await client.change_presence(activity=discord.Activity(
                    type=discord.ActivityType.listening, name=rand_text))

        except Exception as e:
            print("failed to set custom status")
            print(e)
        finally:
            await asyncio.sleep(450)
