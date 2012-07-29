from nmap import nmap
from arp import arp

class network:
    def __init__(self):
        self.nmap = nmap()
        self.arp = arp()

    def get_online_mac_addesses(self):
        ip_list = self.nmap.get_ip_list()
        dictionary = self.arp.get_dictionary()

        mac = []
        for ip in ip_list:
            if ip in dictionary:
                mac.append(dictionary[ip])

        return mac
