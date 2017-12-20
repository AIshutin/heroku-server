#!/usr/bin/python
# -*- coding: utf-8 -*-
import requests
import WebBotTest
last_update_id = 0
API_KEY = "407337744:AAGWltls4FSHvI2yThjcU3qgj68zuAIKcX8"
admin = 0
from time import sleep
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

class PWord:
    name = None
    type = None
    formes = dict()
    char = set()
    def __init__(self, **kwargs):
        for el in kwargs:
            if el == "name":
                self.name = kwargs[el]
            if el == "char":
                self.char = kwargs[el]
            if el == "type":
                self.type = kwargs[el]
            if el == "formes":
                self.formes = kwargs[el]
        
    def __str__(self):
        ans = ["* " + str(self.name) + " *", "Часть речи: " + str(self.type)]
        c = "Характеристика: "
        q = list(self.char)
        for el in q[:-1]:
            c = c + str(el) + ", "
        try:
            c = c + q[-1]
            ans.append(c)
        except:
            pass
        try:
            
            curr = "Формы:"
            if self.type == "существительное":
                curr = curr + "\n" + "Ед. ч.:"
                for el in self.formes[0]:
                    #print(el)
                    curr = curr + "\n" + ' ' * 4 + str(el) + ": " + str(self.formes[0][el])
                curr = curr + "\n" + "Мн. ч.:"
                for el in self.formes[1]:
                    #print(el)
                    curr = curr + "\n" + ' ' * 4 + str(el) + ": " + str(self.formes[1][el])
            elif self.type == "прилагательное":
                for el1 in self.formes:
                    curr = curr + "\n" + str(el1)
                    for q in self.formes[el1]:
                        curr = curr + '\n' + " " * 4 + str(q) + ": " + str(self.formes[el1][q])
                
            elif self.type == "глагол":
                #print(self.formes)
                #exit(0)
                #print(*self.formes)
                for el1 in self.formes:
                    curr = curr + "\n" + str(el1)
                    #print("$")
                    #print(el1, self.formes[el1])
                    #print("#")
                    #sleep(1)
                    for tense in self.formes[el1]:
                        curr = curr + "\n" + " " * 4 + str(tense)
                        #print(tense, self.formes[el1][tense])
                        try:
                            for q in self.formes[el1][tense]:
                                #print(q, self.formes[el1][tense][q])
                                curr = curr + '\n' + " " * 8 + str(q) + ": " + str(self.formes[el1][tense][q])        
                        except:
                            curr = curr + ": " + str(self.formes[el1][tense])
                
            ans.append(curr)
        except Exception as exp:
            print(exp)
        return "\n".join(ans)
    __repr__ = __str__

def sendMessage(text, id):
    data["chat_id"] = id
    data["text"] = text  
    data["parse_mode"] = "Markdown"
    URL = "https://api.telegram.org/bot" + str(API_KEY) + "/sendMessage"
    response = requests.get(URL, data=data)
    
coms = dict()
print(was)
while log:
    # add your code here...
    data = dict()
    data["offset"] = str(last_update_id)
    URL = "https://api.telegram.org/bot" + str(API_KEY) + "/getUpdates"
    response = requests.get(URL, data=data) # make GET request
    updates = response.json()
    for msg in updates['result']:
        try:
            data = dict()
            #print(msg)
            last_update_id = max(last_update_id, int(msg["update_id"]) + 1)
            data["chat_id"] = msg["message"]["chat"]["id"]
            if admin == 0:
                admin = msg["message"]["from"]["id"]
            if msg["message"]["from"]["id"] == admin and len(msg["message"]["text"]) >= 1 and msg["message"]["text"][0] == "/":
                we = msg["message"]["text"]
                if we == "/shutdown":
                    print("XXX")
                    print(last_update_id)
                    print(admin)
                elif we == "/showwords":
                    base.close()
                    fin = open("wordbase.txt", encoding="utf-8")
                    for el in fin.readlines():
                        sendMessage(el, admin)
                    base = open("wordbase.txt", "a", encoding="utf-8")
                    #log = False
                    #break
                elif "/execute" in we:
                    c = len("/execute ")
                    we = we[c:]
                    try:
                        exec(we)
                    except:
                        sendMessage("Failed", admin)
                elif we in coms:
                    coms[we]()
                else:
                    sendMessage("Command not found", admin)
            else:
                q = WebBotTest.webreq(msg["message"]["text"])
                data["text"] = str(PWord(name=q[0], type=q[1], char=q[2], formes=q[3]))
                print("line121", str(q))
                print(q, PWord(name=q[0], type=q[1], char=q[2], formes=q[3]))
                if q != False and q[0] not in was:
                    print(data["text"].replace("\n", ";"), file=base)
                    was.add(q[0])
                sendMessage(data["text"].replace("'", "").replace("[", "").replace("]", ""), data["chat_id"])
        except Exception as err:
            print(err)
                
        #print(msg)
        # add your code here
    #reak
    sleep(1)
    #print("!")

    # sleep here