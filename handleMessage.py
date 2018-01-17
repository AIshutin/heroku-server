def handleMessage(msg):   
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
