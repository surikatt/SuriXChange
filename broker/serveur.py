import paho.mqtt.client as mqtt
import bdd
import json
from datetime import datetime, timedelta
import multiprocessing
from multiprocessing import Manager
import time

from notify_run import Notify 
notify = Notify() 


manager = Manager()
appareils = manager.dict()
time_last_message = manager.dict()

def on_connect(client: mqtt.Client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    #     /#
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#", qos=2)
    print("Connecté!")

def on_message(client, userdata, msg):
    global appareils, time_last_message

    topic = msg.topic
    content = msg.payload.decode("utf-8")
    [type_topic, id_appareil] = topic.split(":")

    print(type_topic)

    print(f"Time: {time_last_message}")
    # time_last_message[id_appareil] = datetime.now()

    if id_appareil not in appareils:
        appareil = bdd.check_apppareil(id_appareil)
        print(f"Appareil trouvé! {appareil}")

    if appareils.get(id_appareil) == False:
        notify.send(f'Appareil reconnecté! ID: {id_appareil}')
        bdd.maj_status(id_appareil, True)

    appareils[id_appareil] = datetime.now()
    
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
    global appareils

    while True:
        print(f"{appareils}")
        for id, date in appareils.items(): 
            print(f"Check: {id}, {date}")
            if date != False and (datetime.now() - date) > timedelta(seconds=10):
                appareils[id] = False
                notify.send(f'Appareil déconnecté! ID: {id}')
                bdd.maj_status(id, False)
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

