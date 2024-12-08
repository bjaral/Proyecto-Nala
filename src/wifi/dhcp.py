import os

os.system("sudo apt-get update")
os.system("sudo apt-get install dnsmasq")

dnsmasq_config = """
interface=wlan0
dhcp-range=192.168.50.10,192.168.50.50,255.255.255.0,12h
dhcp-option=3,192.168.50.1
dhcp-option=6,192.168.50.1
"""

with open('/etc/dnsmasq.conf', 'w') as file:
    file.write(dnsmasq_config)

ip_static_config = """
interface wlan0
static ip_address=192.168.50.1/24
nohook wpa_supplicant
"""

with open('/etc/dhcpcd.conf', 'a') as file:
    file.write(ip_static_config)

os.system("sudo systemctl restart dnsmasq")
os.system("sudo systemctl enable dnsmasq")
os.system("sudo systemctl restart hostapd")
os.system("sudo systemctl enable hostapd")
