from scapy.all import ARP, Ether, IP, srp
import socket

def recup_adress_ip():
    ip_local = IP(dst="0.0.0.0").src
    # print(ip_local)
    target_ip = f"{ip_local}/24"
    arp = ARP(pdst=target_ip)
    ether = Ether(dst="ff:ff:ff:ff:ff:ff")

    packet = ether/arp
    result = srp(packet, timeout=3, verbose=0)[0]

    liste_ip = []
    for sent, received in result:
        liste_ip.append(received.psrc)
    
    return liste_ip

print(recup_adress_ip())

