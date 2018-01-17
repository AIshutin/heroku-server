#!/usr/bin/python
# -*- coding: utf-8 -*-

import requests
from handleMessage import *
import WebBotTest
from time import sleep

last_update_id = 0
API_KEY = "407337744:AAGWltls4FSHvI2yThjcU3qgj68zuAIKcX8"
admin = 0

log = True
was = set()
try:
    fin = open("wordbase.txt", encoding="utf-8")
    for el in fin.readlines():
        if len(el) <= 4:
            continue
        w = el[2:]
        w = w[:w.find("'")]
        was.add(w)
    fin.close()
except:
    pass

base = open("wordbase.txt", "a", encoding="utf-8")

print(was)

while log:
    data = dict()
    data["offset"] = str(last_update_id)
    URL = "https://api.telegram.org/bot" + str(API_KEY) + "/getUpdates"
    response = requests.get(URL, data=data) 
    updates = response.json()
    for msg in updates['result']:
        try:
            data = dict()
            last_update_id = max(last_update_id, int(msg["update_id"]) + 1)
            data["chat_id"] = msg["message"]["chat"]["id"]
            
            if admin == 0:
                admin = msg["message"]["from"]["id"]
            
            handleMessage(msg["message"]["text"], admin == msg["message"]["from"]["id"])
        
        except Exception as err:
            print(err)

    sleep(1)