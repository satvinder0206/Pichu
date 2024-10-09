
import requests
import subprocess
import json
from datetime import datetime
from datetime import timedelta
import discord
import asyncio
from discord import Client


server_url = 'https://cdn2.arkdedicated.com/servers/asa/officialserverlist.json'
rate_url="https://cdn2.arkdedicated.com/asa/dynamicconfig.ini"

def ping_server(ip_address):
   try:
      output = subprocess.check_output(["ping", ip_address])
      return True
   except subprocess.CalledProcessError:
      return False






def find_server(find):
   resp=requests.get(server_url)
   found=False
   if resp.status_code==200:
      data=resp.json()
      for server in data:
         if 'SessionName' in server:
            if find.lower() in server['SessionName'].lower():
               if ping_server(server['IP']):
                  return (
                     f"```Server Is online\n{server['SessionName']}\n"
                     f"IP Address  {server['IP']}\n"
                     f"Daytime  {server['DayTime']}\n"
                     f"Number Of Player  {server['NumPlayers']}```"
                  )
                  found=True
               else:
                  return "Server is Offline"
                  found=True
   if not found:
      return "Server is Not found Or Offline"
   else:
      return "Server is Not found Or Offline"
   


#check rates is changed or not 
last=None
data=None
def loop():
   global last,data
   current_data=requests.get(rate_url).text
   send=None
   if current_data is None or last != current_data:
      with open("channels.json", "r") as file:
            data = json.load(file)
      last=current_data
      return data,current_data,0
   return None,None,1
      




#make record of channel server id and channel id 
def add_server_channel(server_id:str,channel_id:str,role:str):
   try:
      with open("channels.json", "r") as file:
            data = json.load(file)
            for entry in data:
               if entry["server_id"] == server_id:

                     entry["server_id"] = server_id
                     entry["channel_id"] = channel_id
                     entry["role"]=  role
                     print(f"server id {server_id}: {channel_id}")
                     break
            else:
               entry = {"server_id": server_id, "channel_id": channel_id,"role": role}
               print("when data is not avlaible")
               data.append(entry)
   except FileNotFoundError:
      print("file not found")
      data=[]
      entry = {"server_id": server_id, "channel_id": channel_id, "role": role}
      print("when file not found")
      data.append(entry)
   
   with open("channels.json", "w") as file:
      json.dump(data, file)



#add points to user
def addxp(user:str,guild:str,points:int,admin=bool):
   username= user
   flag=0
   delta=timedelta(00,00,00,00,00,00,1,)
   diff=timedelta(00,00,00,00,00,00,1,)
   todays=datetime.today()
   add_points_date=todays.day
   if admin==True:
      add_points_date=add_points_date-7
   try:
      with open(guild+".json", "r") as file:
            data = json.load(file)
            print(data)
            for entry in data:
               if entry["user_id"] == username:
                  date=datetime(int(entry["year"]),int(entry["month"]),int(entry["day"]),int(entry["hr"]),int(entry["min"]))
                  diff=datetime.today()-date
                  print(diff)
                  if  diff>=delta or admin==True:
                     oldxp=entry["xp"]
                     newxp = int(oldxp)+points
                     if newxp<0:
                        flag=1
                        break
                     entry["xp"] = str(newxp)
                     if admin==False:
                        todays=date.today()
                        entry["day"] = str(todays.day)
                        entry["month"] = str(todays.month)
                        entry["year"] = str(todays.year)
                        entry["hr"] = str(todays.hour)
                        entry["min"] = str(todays.minute) 
                     print(f"XP of {username}: {entry['xp']}: {diff.days}")
                     flag=0
                     ent=entry
                     break
                  else:
                     flag=1
                     print(f"you not eligibale")
                  break
            else:
               entry = {"user_id": username, "xp": str(points),"day":str(add_points_date),"month":str(todays.month),"year":str(todays.year),"hr":str(todays.hour),"min":str(todays.minute)}
               print("when data is not avlaible")
               data.append(entry)
   except FileNotFoundError:
      print("file not found")
      data=[]
      todays=datetime.today()
      entry = {"user_id": username, "xp": str(points),"day":str(add_points_date),"month":str(todays.month),"year":str(todays.year),"hr":str(todays.hour),"min":str(todays.minute)}
      print("when file not found")
      data.append(entry)
   
   with open(guild+".json", "w") as file:
      json.dump(data, file)
      return(flag,delta-diff)


#check points by user 
def show_points(user:str,guild:str):
   flag=0
   points=0
   date=datetime.today()
   try:
      with open(guild+".json","r") as file:
         data=json.load(file)
         for entry in data:
            if entry["user_id"] == user:
               date=datetime(int(entry["year"]),int(entry["month"]),int(entry["day"]),int(entry["hr"]),int(entry["min"]))
               points=entry["xp"]
               flag=0
            else:
               points=0
               date=datetime.today()
               flag=1

   except FileNotFoundError:
      flag=1
   return(flag,date,points)
