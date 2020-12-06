#!/usr/bin/env python3
# This python script scans the present network connected to, and shows the IPs and MACs of the devices connected.

import scapy.all as scapy
import optparse


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--ipaddress", dest="ipaddress", help="The IP Address for Scanning")
    options, arguments = parser.parse_args()
    if not options.ipaddress:
        print("[-] Please enter the IP Address")
    else:
        return options


def scan(ipaddress):
    arp_req = scapy.ARP(pdst=ipaddress)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_req_broadcast = broadcast/arp_req
    answered_list = scapy.srp(arp_req_broadcast, timeout=1, verbose=False)[0]
    client_list = []
    for element in answered_list:
        client_dict = {"ip": element[1].psrc, "mac": element[1].hwsrc}
        client_list.append(client_dict)
        return client_list


def print_list(result_list):
    print("----------------------------------------------------------------")
    print("IP\t\t|\tMAC Address")
    print("----------------------------------------------------------------")
    for client in result_list:
        print(client["ip"] + "\t\t" + client["mac"])
        print("----------------------------------------------------------------")


ip = get_arguments()
scan_result = scan(ip.ipaddress)
print_list(scan_result)
