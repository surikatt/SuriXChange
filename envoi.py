import json
import socket
import uuid

from scapy.all import ARP, Ether, IP, srp
import socket

def recup_adresses_ip():
    ip_locale = IP(dst="0.0.0.0").src
    # print(ip_local)
    target_ip = f"{ip_locale}/24"
    arp = ARP(pdst=target_ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")

    packet = ether/arp
    result = srp(packet, timeout=3, verbose=0)[0]

    liste_ip = []
    for sent, received in result:
        liste_ip.append(received.psrc)
    
    return liste_ip


port = 8000

ip_locale = IP(dst="0.0.0.0").src
liste = recup_adresses_ip() 
liste.append(ip_locale) # à retirer

for host in liste:
    try:
        print(f"Connexion à {host}...")
        client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client.settimeout(2)
        client.connect((host, port))
        print(f"Connexion réussie avec l'hôte {host}")
        message = "Bonjour, Raspberry Pi récepteur!"
        mac = hex(uuid.getnode())[2:].upper()  # Obtenir l'adresse MAC de l'émetteur
        data = json.dumps({'mac': mac, 'message': message}).encode('utf-8')
        client.sendall(data)
        client.close()
        break  # Sortir de la boucle si la connexion réussit
    except:
        print(f"Impossible de se connecter à l'hôte {host}")
        

print("Terminé.")


"""
host = ''  # Adresse IP du Raspberry Pi récepteur
port = 8000
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

def envoyer_message(type_message):
    mac = hex(uuid.getnode())[2:].upper()  
    data = json.dumps({'type': type_message, 'mac': mac}).encode('utf-8')
    client.sendall(data)

envoyer_message('ouverture')
"""