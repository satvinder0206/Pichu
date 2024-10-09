
import discord
import json
import os
import re
import functions1
from discord.ext import commands
from discord import Interaction
from discord import app_commands
from discord.utils import get
from discord import User
from discord import TextChannel
import requests
from datetime import datetime
from datetime import timedelta
import random
import asyncio
from discord import Role
import concurrent.futures
from main import generate_image


msgs=["message0","message1","message2","message3","message4","message5","message6","message7","message8","message9"]


my_secret = 'your Bot token here'
rate_url="https://cdn2.arkdedicated.com/asa/dynamicconfig.ini"
spot_clid='91d3c244469a4244b15e53d91e4ca901'
spot_cs='d71d242741414d30b7dbc319e48d0c58'



bot = commands.Bot(command_prefix="!", intents = discord.Intents.all())
@bot.event
async def on_ready():
  print('We have logged in as {0.user}')
  try:
     synced = await bot.tree.sync()
     print(f"Synced {len(synced)} command(s)")
     #await ratecheck()
     

  except Exception as e:
      print(e)
async def setup_hook(self):
        await self.tree.sync()
#intervel rates check
async def ratecheck():
   serverlist,data,flag=functions1.loop()
   if flag==0:
      pattern = r"^\s*([\w.]+)\s*=\s*([\w.-]+)\s*$"
      keys = []
      values = []
      img=bot.application.icon
      for line in data.split('\n'):
         match = re.match(pattern, line)
         if match:
            key, value= match.groups()
            keys.append(key)
            values.append(value)
   
      for ent in serverlist:
         try:
            guild=bot.get_guild(int(ent['server_id']))
            channel=guild.get_channel(int(ent['channel_id']))
            role=guild.get_role(int(ent['role']))   
            emb=discord.Embed(
            title= 'Ark ascended Official server Rates',
            description=(f"**{keys[0]}** = {values[0]}\n**{keys[1]}** = {values[1]} \n**{keys[2]}** = {values[2]}\n**{keys[3]}** = {values[3]}\n**{keys[4]}** = {values[4]}\n**{keys[5]}** = {values[5]}\n**{keys[6]}** = {values[6]}\n**{keys[7]}** = {values[7]}"),
            colour=discord.Colour.pink()
            )
            emb.set_thumbnail(url=f"{img}")
            await channel.send(embed=emb)
            await channel.send(role.mention)
         except KeyError:
            print("server channel missing or went somethibg wrong")
      await asyncio.sleep(300)  # 300 seconds = 5 minutes
      await ratecheck()
   


@bot.tree.command(name="rates", description="Ark Official server Rates")
async def rates(int: discord.Interaction):
  rate=requests.get(rate_url).text
  config_data = {}
  pattern = r"^\s*([\w.]+)\s*=\s*([\w.-]+)\s*$"
  keys = []
  values = []
  img=int.client.application.icon
  for line in rate.split('\n'):
        match = re.match(pattern, line)
        if match:
            key, value = match.groups()
            keys.append(key)
            values.append(value)
  
  emb=discord.Embed(
     title= 'Ark ascended Official server Rates',
     description=(f"**{keys[0]}** = {values[0]}\n**{keys[1]}** = {values[1]} \n**{keys[2]}** = {values[2]}\n**{keys[3]}** = {values[3]}\n**{keys[4]}** = {values[4]}\n**{keys[5]}** = {values[5]}\n**{keys[6]}** = {values[6]}\n**{keys[7]}** = {values[7]}"),
     colour=discord.Colour.pink()
   )
  emb.set_thumbnail(url=f"{img}")
  await int.response.send_message(embed=emb)
   

@bot.tree.command(name="set_rate_channel",description="set server channel for auto XP rates ")
@app_commands.describe(channel="Text channel")
@app_commands.describe(role="role to mention")
@app_commands.checks.has_permissions(administrator=True)
async def set_rate_channel(int:discord.Integration,channel:TextChannel,role:Role):
   functions1.add_server_channel(str(int.guild.id),str(channel.id),str(role.id))
   await channel.send("this channel is been set for auto respond for Official rates")
   await int.response.send_message(f"{channel.mention} is set for auto rates response ")

#image gentaror

def heavy_task(prompt,steps):
    # Simulate a heavy task (like image generation)
    import time
    time.sleep(3)  # Simulate delay
    image = generate_image(prompt,steps)
    return image
    
async def generate_image1(prompt,steps,guildid,chanid,userid):
   loop=asyncio.get_event_loop()
   with concurrent.futures.ThreadPoolExecutor() as pool:
         result =await loop.run_in_executor(pool, heavy_task, prompt,steps)
   result.save("image.png")
   guild=bot.get_guild(int(guildid))
   channel=guild.get_channel(int(chanid))
   user=guild.get_member(int(userid))
   #await channel.send(user.mention)
   await channel.send(file=discord.File("image.png"))
   #await int.followup.send(int.user.mention)
   os.remove("image.png")

   
@bot.tree.command(name="genimage",description="generate image")
@app_commands.describe(prompt="prompt")
@app_commands.describe(steps="steps")
async def set_rate_channel(int: discord.Integration,prompt: str,steps: int):
   await int.response.send_message("Generating your image this might take While \nplease wait...",ephemeral=True)
   chanid=int.channel.id
   guildid=int.guild.id
   userid=int.user.id
   await generate_image1(prompt,steps,guildid,chanid,userid)


@bot.tree.command(name="asa", description="Check server status")
@app_commands.describe(server="server")
async def asa(int: discord.Interaction,server:str):
   await int.response.send_message(f"**Serching For Server** {server}\n-------------------------------")
   result=functions1.find_server(server)
   await int.channel.send(result)




@bot.tree.command(name="claim", description="to claim The XP")
async def claim(int: discord.Integration):

   flag,cooldown=functions1.addxp(str(int.user.id),str(int.guild.id),60,False)
   if flag==0:
      await int.response.send_message("Points been Credit")
   else:
      await int.response.send_message(f"You already Claimed this weeks points Please try again in {cooldown.days} days {cooldown.seconds//3600} hours {(cooldown.seconds//60)%60} min" )

@bot.tree.command(name="balance",description="To check how much points you have")
async def balance(int: discord.Integration):
   flag,date,points=functions1.show_points(str(int.user.id),str(int.guild.id))
   if flag==0:
      await int.response.send_message(f"Your claimed points is : {points} last claimed date : {date}")
   else:
      await int.response.send_message("you haven't claimed any points")


@bot.tree.command(name="user_balance",description="To check how much points you have")
@app_commands.describe(username="username")
@app_commands.checks.has_permissions(administrator=True)
async def user_balance(int: discord.Integration,username:User):
   flag,date,points=functions1.show_points(str(username.id),str(int.guild.id))
   if flag==0:
      await int.response.send_message(f"{username.name}'s claimed points is : {points} last claimed date : {date}")
   else:
      await int.response.send_message("user haven't claimed any points")


@bot.tree.command(name="add_points",description="To add opints to user account")
@app_commands.describe(username="username")
@app_commands.describe(points="points")
@app_commands.checks.has_permissions(administrator=True)
async def add_points(int:discord.Integration,username:User,points:int):
   userid=username.id
   flag,date=functions1.addxp(str(userid),str(int.guild.id),points,True)
   if flag==0:
      await int.response.send_message(f"{username.mention} You recived {points} Points")
   else:
      await int.response.send_message(f"Adding points failed try again" ,ephemeral=True )
   

@bot.tree.command(name="remove_points",description="To remove opints to user account")
@app_commands.describe(username="username")
@app_commands.describe(points="points")
@app_commands.checks.has_permissions(administrator=True)
async def remove_points(int:discord.Integration,username:User,points:int):
   userid=username.id
   flag,date=functions1.addxp(str(userid),str(int.guild.id),-points,True)
   if flag==0:
      await int.response.send_message(f"{username.mention} You redeemed {points} Points")
   else:
      await int.response.send_message(f"removing points failed try again please check how much points user have " ,ephemeral=True )   


@bot.tree.command(name="show_tips",description="show tips")
async def show_tips(int:discord.Integration):
   msg=random.choice(msgs)
   await int.response.send_message(f"tips",ephemeral=True )
   await int.channel.send(f"{msg}")

@bot.tree.command(name="ban_user",description="ban user account")
@app_commands.describe(username="username")
@app_commands.describe( reson="reason")
@app_commands.checks.has_permissions(administrator=True)
async def remove_points(int:discord.Integration,username:User,reson:str):
   await int.guild.ban(user=username,reason=reson)
   await int.response.send_message(f"user {username} is banned ",ephemeral=True )
   await int.channel.send(f"user {username} is banned Reason: {reson}")



@bot.event
async def on_message(message):
   if message.content.lower()=='singh':
      await message.channel.send("hello")
    

@bot.tree.command(name="twitch", description="Singh FPS Twich Link")
async def admin(int: discord.Integration):
   user=await int.user.create_dm()
   await user.send("https://www.twitch.tv/singh_fps")
   await int.response.send_message(f"{int.user.mention}Link is in your DM")



@bot.tree.error
async def on_app_commandError(int:discord.Interaction,error):
   await int.response.send_message(error,ephemeral=True)

  
bot.run(my_secret)

