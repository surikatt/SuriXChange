import json
import socket
import uuid


host = ''  # Adresse IP du Raspberry Pi récepteur
port = 8000
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

def envoyer_message(type_message):
    mac = hex(uuid.getnode())[2:].upper()  
    data = json.dumps({'type': type_message, 'mac': mac}).encode('utf-8')
    client.sendall(data)


def envoyer_ouverture():
    envoyer_message('ouverture')


"""
from scapy.all import ARP, Ether, srp

# Fonction pour scanner le réseau local et retourner une liste d'adresses IP disponibles
def scanner_reseau_local():
    arp = ARP(pdst='192.168.1.1/24')  # Définir la plage d'adresses IP à scanner
    ether = Ether(dst='ff:ff:ff:ff:ff:ff')
    packet = ether/arp
    result = srp(packet, timeout=3, verbose=0)[0]
    return [r[1].psrc for r in result]

# Trouver l'adresse IP de l'hôte sur le réseau local et se connecter à lui
adresses_disponibles = scanner_reseau_local()
if len(adresses_disponibles) > 0:
    host = adresses_disponibles[0]  # Utiliser la première adresse IP disponible
    port = 8000
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))
else:
    print("Aucun hôte disponible sur le réseau local.")
"""