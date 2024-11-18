#hay que instalar un dhcp
#preguntar al profe de esta parte del codigo, no si se realmente este correcto lo que estoy haciendo, aclar duda en la clase del martes URGENTE
# sudo apt-get update
#sudo apt-get install dnsmasq
#Configuracion del dnsmasq
#interface=wlan0              # Usa la interfaz wlan0 (puedes cambiarla si es necesario)
#dhcp-range=192.168.50.10,192.168.50.50,255.255.255.0,12h # Rango de IPs (de .10 a .50)
#dhcp-option=3,192.168.50.1   # Puerta de enlace (en este caso, la IP de tu Raspberry Pi)
#dhcp-option=6,192.168.50.1   # Servidor DNS (puedes poner la IP de la Raspberry Pi o de un servidor DNS público)
#Configuración de IP estática para la interfaz wlan0:
#sudo nano /etc/dhcpcd.conf
#interface wlan0
#static ip_address=192.168.50.1/24   # Dirección IP estática para wlan0
#nohook wpa_supplicant
#Iniciar el servicio dnsmasq
#sudo systemctl restart dnsmasq
# este codigo es en caso de que se requiera que se active al arrancar sudo systemctl enable dnsmasq
#Iniciar el servicio hostapd (si no está corriendo ya):

#El servicio hostapd es el que gestiona el punto de acceso en la Raspberry Pi. Si ya configuraste hostapd (como en el Código 1), asegúrate de que se reinicie también:

#todo esto es en el bash, bueno en general todos los codigos que agrege son para el bash, pero bueno xd , a
#Copiar código
#sudo systemctl restart hostapd
#Y habilítalo para que se inicie al arrancar:


#Copiar código
#sudo systemctl enable hostapd
