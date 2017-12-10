import requests
last_update_id = 0
API_KEY = "407337744:AAGWltls4FSHvI2yThjcU3qgj68zuAIKcX8"
admin = 0
from time import sleep
log = True
while log:
    # add your code here...
    data = dict()
    data["offset"] = str(last_update_id)
    URL = "https://api.telegram.org/bot" + str(API_KEY) + "/getUpdates"
    response = requests.get(URL, data=data) # make GET request
    updates = response.json()
    for msg in updates['result']:
        data = dict()
        print(msg)
        last_update_id = max(last_update_id, int(msg["update_id"]) + 1)
        data["chat_id"] = msg["message"]["chat"]["id"]
        data["text"] = "I am alive4"
        #print(msg["message"]["text"], msg["message"]["from"]["id"], msg["message"]["text"] == "/shutdown", msg["message"]["from"]["id"] == "438162308")
        #print(msg["message"]["from"]["id"] == int(msg["message"]["from"]["id"]))
        if admin == 0:
            admin = msg["message"]["from"]["id"]
        if msg["message"]["text"] == "/shutdown" and msg["message"]["from"]["id"] == admin:
            print("XXX")
            log = False
            break
        URL = "https://api.telegram.org/bot" + str(API_KEY) + "/sendMessage"
        response = requests.get(URL, data=data) # make GET request
        #print(msg)
        # add your code here
    #reak
    sleep(1)
    #print("!")

    # sleep here