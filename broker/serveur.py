import paho.mqtt.client as mqtt
import bdd
import json
from datetime import datetime, timedelta
import multiprocessing
from multiprocessing import Manager
import time

appareils_connectes = []


manager = Manager()
time_last_message = manager.dict()

def on_connect(client: mqtt.Client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    #     /#
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#", qos=2)
    print("Connecté!")

def on_message(client, userdata, msg):
    global appareils_connectes, time_last_message

    topic = msg.topic
    content = msg.payload.decode("utf-8")
    [type_topic, id_appareil] = topic.split(":")

    print(type_topic)

    print(f"Time: {time_last_message}")
    time_last_message[id_appareil] = datetime.now()


    if topic not in appareils_connectes:
        appareils_connectes.append(topic)
        appareil = bdd.check_apppareil(id_appareil)
        print(f"Appareil trouvé! {appareil}")
    
    if type_topic == "idcarte":
        utilisateur = bdd.check_idcarte(content)
        if utilisateur == None:
            print("Utilisateur non autorisé!")
            return
        print(f"Utilisateur trouvé: {utilisateur}")
    
    if type_topic == "telephone":
        if json.loads(content) == {"type": "requete", "requete": "appareils"}:
            appareils = bdd.recuperer_appareils()
            data = {"type": "appareils", "data": appareils}
            client.publish(topic, json.dumps(data), qos=1)

    if type_topic == "contacteur":
        if content == "0":
            print("test")
        if content == "1":
            print("test1")

    print(f"Topic: {topic}; ID: {id_appareil}; MSG: {content}")

def check_ping():
    global time_last_message

    while True:
        for id, date in time_last_message.items(): 
            if (datetime.now() - date) > timedelta(seconds=60):
                ...
        time.sleep(5)

process_ping = multiprocessing.Process(target=check_ping)
process_ping.start()

client = mqtt.Client(reconnect_on_failure=True)
client.on_connect = on_connect
client.on_message = on_message

client.connect("172.16.26.102", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()          

