import requests
from handleMessage import *
import WebBotTest


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
                for el1 in self.formes:
                    curr = curr + "\n" + str(el1)
                    for tense in self.formes[el1]:
                        curr = curr + "\n" + " " * 4 + str(tense)
                        try:
                            for q in self.formes[el1][tense]:
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


def handleMessage(msg, isAdmin):  
    if isAdmin and len(msg) >= 1 and msg == "/":
        if msg == "/shutdown":
            print("XXX")
            print(last_update_id)
            print(admin)
        elif msg == "/showwords":
            base.close()
            fin = open("wordbase.txt", encoding="utf-8")
            for el in fin.readlines():
                sendMessage(el, admin)
            base = open("wordbase.txt", "a", encoding="utf-8")
        elif "/execute" in msg:
            c = len("/execute ")
            msg = msg[c:]
            try:
                exec(msg)
            except:
                sendMessage("Failed", admin)
        else:
            return "Command not found"
    else:
        q = WebBotTest.webreq(msg)
        data["text"] = str(PWord(name=q[0], type=q[1], char=q[2], formes=q[3]))
        print("line121", str(q))
        print(q, PWord(name=q[0], type=q[1], char=q[2], formes=q[3]))
        if q != False and q[0] not in was:
            print(data["text"].replace("\n", ";"), file=base)
            was.add(q[0])
        return (data["text"].replace("'", "").replace("[", "").replace("]", ""), data["chat_id"])
