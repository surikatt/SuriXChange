import paho.mqtt.client as mqtt
import bdd
import json
from datetime import datetime, timedelta
import multiprocessing
from multiprocessing import Manager, Process
import time
import ihm
import RPi.GPIO as GPIO

from notify_run import Notify
notify = Notify()

manager = Manager()
appareils = manager.dict()
en_alerte = multiprocessing.Value('i', False)
est_armee = multiprocessing.Value('i', False)
alarme_proc = None
buzzer_en_marche: multiprocessing.Value = multiprocessing.Value('i', False)

buzzer = 2
pinBtn = 18
led = 3

GPIO.setmode(GPIO.BCM)
GPIO.setup(pinBtn, GPIO.IN, pull_up_down=GPIO.PUD_UP)


def sonner_buzzer():
    global buzzer_en_marche
    while buzzer_en_marche.value:
        print("Buzzer: ", buzzer_en_marche)
        bdd.ajout_evenement("centrale", "Sonne")
        GPIO.output(led, GPIO.HIGH)
        GPIO.output(buzzer, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(led, GPIO.LOW)
        GPIO.output(buzzer, GPIO.LOW)
        time.sleep(1)


def bouton_appuye(a=0):
    global est_armee
    if est_armee.value:
        return
    print("potatoes")
    ihm.buzzer_correct()
    ihm.led_on()
    est_armee.value = True
    bdd.ajout_evenement("centrale", "armement")


GPIO.add_event_detect(pinBtn, GPIO.RISING,
                      callback=bouton_appuye, bouncetime=200)


def alarme():
    global en_alerte, alarme_proc, buzzer_en_marche
    time.sleep(10)
    en_alerte.value = True
    print("Alarme")
    buzzer_en_marche.value = True
    Process(target=sonner_buzzer).start()


def desarmer():
    global en_alerte, est_armee, buzzer_en_marche

    print("DESARMEMENT")
    print(buzzer_en_marche)
    buzzer_en_marche.value = False
    print(buzzer_en_marche)
    en_alerte.value = False
    est_armee.value = False
    bdd.ajout_evenement("centrale", "desarmement")


def on_connect(client: mqtt.Client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    #     /#
    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("#", qos=2)
    print("Connecté!")


def on_message(client, userdata, msg):
    global appareils, est_armee, alarme_proc, en_alerte

    topic = msg.topic

    if topic == "evenements":
        return

    content = msg.payload.decode("utf-8")
    [type_topic, id_appareil] = topic.split(":")

    print(type_topic)
    # time_last_message[id_appareil] = datetime.now()

    if type_topic == "telephone":
        data = json.loads(content)
        if data == {"type": "requete", "requete": "appareils"}:
            data_appareils = bdd.recuperer_appareils()
            data = {"type": "appareils", "data": data_appareils}
            client.publish(topic, json.dumps(data), qos=1)
        elif data == {"type": "requete", "requete": "evenements"}:
            data_evenements = bdd.recuperer_evenements()
            data = {"type": "evenements", "data": data_evenements}
            client.publish(topic, json.dumps(data), qos=1)
        elif data["type"] == "armement":
            bouton_appuye()
        return

    if id_appareil not in appareils:
        appareil = bdd.check_apppareil(id_appareil)
        print(f"Appareil trouvé! {appareil}")

    if appareils.get(id_appareil) == False:
        notify.send(f'Appareil reconnecté! ID: {id_appareil}')
        bdd.maj_status(id_appareil, True)
        envoyer_statut(id_appareil, True)

    appareils[id_appareil] = datetime.now()

    if type_topic == "idcarte" and (est_armee.value or buzzer_en_marche.value or en_alerte.value):
        utilisateur = bdd.check_idcarte(content)
        if utilisateur == None:
            print("Utilisateur non autorisé!")
            Process(target=ihm.buzzer_incorrect).start()
            bdd.ajout_evenement("utisateur", "non autorisé")
            return
        Process(target=ihm.buzzer_correct).start()
        print(alarme_proc)
        if not alarme_proc == None:
            alarme_proc.kill()
        print(f"Utilisateur trouvé: {utilisateur}")
        bdd.ajout_evenement("utilisateur", "autorisé")
        desarmer()
        Process(target=ihm.led_off).start()

    if type_topic == "mouvement":
        en_alerte.value = True

    if type_topic == "contacteur" and not en_alerte.value and est_armee.value:
        if content == "0":
            bdd.ajout_evenement(id_appareil, "fermeture")
        if content == "1":
            bdd.ajout_evenement(id_appareil, "ouverture")
            alarme_proc = Process(target=alarme)
            alarme_proc.start()

    print(f"Topic: {topic}; ID: {id_appareil}; MSG: {content}")


client = mqtt.Client(reconnect_on_failure=True)


def envoyer_statut(id_appareil: str, connecte: bool):
    print(f"Publish {id_appareil} {connecte}")
    data = json.dumps({
        "type": "maj",
        "appareil": id_appareil,
        "connecte": connecte
    })

    client.publish("evenements", data, qos=2)


def check_ping():
    global appareils

    while True:
        # print(f"Check: {len(appareils)}")
        for id, date in appareils.items():
            # print(f"Check: {id}, {date}")
            if date != False and (datetime.now() - date) > timedelta(seconds=25):
                appareils[id] = False
                print("Deconnecté")
                envoyer_statut(id, False)
                # notify.send(f'Appareil déconnecté! ID: {id}')
                bdd.maj_status(id, False)
        time.sleep(5)


process_ping = multiprocessing.Process(target=check_ping)
process_ping.start()

client.on_connect = on_connect
client.on_message = on_message

# client.loop_start()

client.connect("172.16.26.102", 1883, 60)
client.loop_forever()

# Blocking call that processes network traffic, dispatches callbacks and
# handles reconnecting.
# Other loop*() functions are available that give a threaded interface and a
# manual interface.
