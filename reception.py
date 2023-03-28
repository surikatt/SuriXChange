import json
import socket
import time

# Définir les informations de connexion
host = ''  # Adresse IP locale du Raspberry Pi récepteur
port = 8000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(1)

# Fonction pour traiter les messages reçus
def traiter_message(data):
    message = json.loads(data.decode('utf-8'))
    type_message = message['type']

    if type_message == "connection":
        print("Nouvelle connection")
    elif type_message == "ouverture":
        pass

    print(f"{message}")
    mac = message['mac']
    # message_recu = message['message']
    print("Adresse MAC de l'émetteur:", mac)
    # print("Message reçu:", message_recu)

# Boucle principale pour écouter les connexions entrantes et traiter les messages
while True:
    conn, addr = server.accept()
    data = conn.recv(1024)
    if len(data) != 0:
        traiter_message(data)
    conn.close() # a retirer sur serveur