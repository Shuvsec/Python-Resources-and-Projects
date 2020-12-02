#!/usr/bin/env python
# This script changes the MAC Address and takes the Interface and New Mac Address as input

import subprocess
import optparse
import re


def get_arguments():
    parser = optparse.OptionParser()
    parser.add_option("-i", "--interface", dest="interface", help="Interface to change the MAC Address")
    parser.add_option("-m", "--mac", dest="mac_addr", help="New MAC Address")
    (options, arguments) = parser.parse_args()
    if not options.interface:
        parser.error("[!] Please specify an Interface, use --help for more info")
    elif not options.mac_addr:
        parser.error("[!] Please specify a new MAC Address, use --help for more info")
    else:
        return options


def change_mac(interface, mac_addr):
    print("[+] Changing MAC Address for " + interface + " to " + mac_addr)
    subprocess.call(["ifconfig", interface, "down"])
    subprocess.call(["ifconfig", interface, "hw", "ether", mac_addr])
    subprocess.call(["ifconfig", interface, "up"])


def get_current_mac(interface):
    ifconfig_result = subprocess.check_output(["ifconfig", interface])
    mac_addr_result = re.search(r"\w\w:\w\w:\w\w:\w\w:\w\w:\w\w", str(ifconfig_result))

    if mac_addr_result:
        return mac_addr_result.group(0)
    else:
        print("[!] Could not read MAC Address.")


options = get_arguments()
current_mac = get_current_mac(options.interface)
print("Current MAC Address = ", str(current_mac))
change_mac(options.interface, options.mac_addr)

current_mac = get_current_mac(options.interface)
if current_mac == options.mac_addr:
    print("[+] MAC Address has been successfully changed to " + current_mac)
else:
    print("[!] MAC Address could not be changed.")
