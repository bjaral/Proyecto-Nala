import os
import threading

# Configuración de hostapd (Punto de acceso Wi-Fi)
hostapd_config = f"""
interface=ap0
ssid=sincomilla
wpa_passphrase=12345678
driver=nl80211
hw_mode=g
channel=6
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=CCMP
rsn_pairwise=CCMP
"""

# Función para iniciar hostapd
def init_hostapd():
    # Crear el archivo de configuración de hostapd
    with open('/etc/hostapd/hostapd.conf', 'w') as file:
        file.write(hostapd_config)

    # Iniciar hostapd para crear el punto de acceso
    os.system("sudo hostapd /etc/hostapd/hostapd.conf")

# Función para configurar dnsmasq (DHCP y DNS)
def DHCP_DNS():
    # Configurar dnsmasq para proporcionar DHCP y DNS
    os.system("sudo dnsmasq -C /dev/null -kd -F 192.168.4.2,192.168.4.20 -i ap0 --bind-dynamic")

# Crear hilos para ejecutar ambas funciones simultáneamente
hilo1 = threading.Thread(target=init_hostapd)
hilo2 = threading.Thread(target=DHCP_DNS)

# Iniciar los hilos
hilo1.start()
hilo2.start()

# Habilitar el reenvío de IP para permitir el acceso a Internet
os.system("sudo sysctl net.ipv4.ip_forward=1")

# Configurar NAT para el enrutamiento de paquetes
os.system("sudo iptables -t nat -A POSTROUTING -o eth0 -j MASQUERADE")
