import json
import socket

host = ''  # Adresse IP du Raspberry Pi récepteur (vide pour accepter toutes les connexions)
port = 8000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(1)

print(f"En attente de connexions sur le port {port}...")

while True:
    conn, addr = server.accept()
    print(f"Connexion acceptée de {addr[0]}:{addr[1]}")
    data = conn.recv(1024)
    if data:
        message = json.loads(data.decode('utf-8'))['message']
        print(f"Message reçu: {message}")
    conn.close()

"""
host = ''  # rien = ecoute sur la machine ou le code s'execute
port = 8000
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(1)


def traiter_message(data):
    message = json.loads(data.decode('utf-8'))
    type_message = message['type']
    print(f"{message}")



# Boucle principale pour écouter les connexions entrantes et traiter les messages
while True:
    conn, addr = server.accept()
    data = conn.recv(1024)
    if len(data) != 0:
        traiter_message(data)
    conn.close() # a retirer sur serveur
"""