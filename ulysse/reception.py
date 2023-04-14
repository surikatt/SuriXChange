import json
import socket
import multiprocessing

host = ''  # Adresse IP du Raspberry Pi récepteur (vide pour accepter toutes les connexions)
port = 8000

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((host, port))
server.listen(1)

print(f"En attente de connexions sur le port {port}...")

def gerer_connexion(connexion: socket.socket):
    print(f"Connexion acceptée de {addr[0]}:{addr[1]}")

    while True:
        longueur = int.from_bytes(conn.recv(32), byteorder='big')
        data = conn.recv(longueur)
        
        if data and len(data) != 0:
            data = json.loads(data.decode('utf-8'))
            message = data['message']

            if message == "connexion":
                print(f"Nouvelle connexion de: {data['mac']}, type: {data['type_appareil']}") 
                # rajouter dans base de donner
            print(f"Message reçu: {message}")
            # modifier bas de donner en consequence


while True:
    conn, addr = server.accept()
    multiprocessing.Process(target=gerer_connexion, args=[conn]).start()
    conn.close()
