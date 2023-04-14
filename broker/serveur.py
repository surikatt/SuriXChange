import paho.mqtt.client as mqtt
import bdd
import json

appareils_connectes = []

def on_connect(client: mqtt.Client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    #     /#
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#", qos=2)
    print("Connecté!")

def on_message(client, userdata, msg):
    global appareils_connectes

    topic = msg.topic
    content = msg.payload.decode("utf-8")
    [type_topic, id_appareil] = topic.split(":")

    print(type_topic)

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
        if content == "appareils":
            donnee = list(bdd.recuperer_appareils())
            print(donnee)
            data = {"type": "appareils", "data": donnee}
            client.publish(topic, json.dumps(data))

    if type_topic == "contacteur":
        if content == "0":
            print("test")
        if content == "1":
            print("test1")

    print(f"Topic: {topic}; ID: {id_appareil}; MSG: {content}")

client = mqtt.Client(reconnect_on_failure=True)
client.on_connect = on_connect
client.on_message = on_message

client.connect("172.16.26.102", 1883, 60)

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
client.loop_forever()          

