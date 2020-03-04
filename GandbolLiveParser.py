#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import re
import json


# In[2]:


import telebot
from telebot import types
bot = telebot.TeleBot("939202590:AAFGvkADtvtsGvhABm_Br1L16H4ThaQV7z0")


# In[8]:


def get_page():
    page  = requests.get("https://1xbet.cr/ru/live/Handball/").text  
    return BeautifulSoup(page, 'html5lib')


# In[9]:


import requests

def get_live_info():
    cookies = {'enwiki_session': '17ab96bd8ffbe8ca58a78657a918558'}

    params={
        "sports": 8,
        "count": 50,
        "antisports": 198,
        "mode": 4,
        "country": 40,
        "getEmpty": True
    }

    headers={
        "Accept": "*/*",
        "DNT": "1",
        "Referer": "https://1xbet.cr/ru/live/Handball/",
        "Sec-Fetch-Mode": "cors",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
        "X-Requested-With": "XMLHttpRequest"


    }

    page  = requests.get("https://1xbet.cr/LiveFeed/Get1x2_VZip",params=params,headers=headers).text  
    try:
        return json.loads(page)
    except:
        print(requests.get("https://1xbet.cr/LiveFeed/Get1x2_VZip",params=params,headers=headers))
        print("ERROR",page)
        exit(-1)


# In[10]:


bet_ids=[]


# In[ ]:


from datetime import datetime
import time
nom=0

while True:
    info = get_live_info()
    if nom%10==0:
        soup = get_page()
    
    for i in info["Value"]:
        if len(i["SC"]["PS"])>1:
            m1=i["SC"]["PS"][0]["Value"]["S1"]
            m2=i["SC"]["PS"][0]["Value"]["S2"]  
            if min(m1,m2)<14 and m1+m2 < 31:
                match={}
                liga = i["L"]
                country = i["CN"]
                game = i["O1"]+" - "+i["O2"]
                match_id=i["I"]
                url = "https://1xbet.cr/ru/"+soup.find("a",href=re.compile(str(i["I"])))["href"]        

                win=1
                if m1>m2:
                    win=2

                bets={}
                for bet in i["E"]:
                    if bet["T"]==1:
                        bets["Win1"]=1/bet["C"]
                    elif bet["T"]==3:
                        bets["Win2"]=1/bet["C"]
                    elif bet["T"]==9:
                        bets["Total"]=bet["P"]
                        bets["TotalMore"]=bet["C"]  
                    elif bet["T"]==10:
                        bets["TotalLess"]=bet["C"] 

                    elif bet["T"]==11+2*(win-1):
                        bets["Total_player"]=bet["P"] 
                        bets["Total_player_less"]=bet["C"] 
                    elif bet["T"]==12+2*(win-1):
                        bets["Total_player_more"]=bet["C"] 

                match["id"]=i["i"]
                match["bet"]=bet
                match["url"]=url
                match["games"]=i["SC"]["PS"]
                match["time"]=datetime.now()

                with open("films.jsonlines","a") as f:
                        f.write(json.dumps(film,ensure_ascii=False)+"\n")

                if i["I"] not in bet_ids:
                    bet_ids.append(i["I"])

                    print(game,": ИТБ-"+str(win),min(m1,m2)*2-0.5,liga)
                    print(bets["Total_player"],bets["Total_player_more"])
                    print("")

                    markup = types.InlineKeyboardMarkup()
                    markup.add(types.InlineKeyboardButton(text="Открыть матч", url=url))
                    bot.send_message(chat_id="@betparse",
                                                     parse_mode="HTML",
                                                     reply_markup=markup,
                                                     text=game+": ИТБ-"+str(win)+str(min(m1,m2)*2-0.5)+liga )

    time.sleep(5)
    print("---")
    nom+=1

