import json
import socket
import uuid
from scapy.all import ARP, Ether, IP, srp

port = 8000

def recup_adresses_ip_toute():
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

def recuperer_connexion():
    ip_locale = IP(dst="0.0.0.0").src #
    liste = recup_adresses_ip_toute() #
    liste.append(ip_locale)           # à retirer sur central

    for host in liste:
        try:
            #print(f"Connexion à {host}...")
            client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            client.settimeout(2)
            client.connect((host, port))
            #print(f"Connexion réussie avec l'hôte {host}")
            print("ggggggggggggggggggggggggg")
            return client
        except:
            pass    # adresse != centrale

client = recuperer_connexion()
mac = hex(uuid.getnode())[2:].upper()  

def envoyer_message(message, autres = {}, ):
    data = json.dumps({'message': message, 'mac': mac} | autres).encode('utf-8')
    client.sendall(data)

envoyer_message("connexion", {'type_appareil': "camera"})
envoyer_message("ouverture")

client.close()