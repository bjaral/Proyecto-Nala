import os
import subprocess

def escanear_redes():
    print("Escaneando redes Wi-Fi disponibles en los alrededores")
    redes = set()
    try:
        resultado = subprocess.check_output(["sudo", "iwlist", "wlan0", "scan"], universal_newlines=True)
        for linea in resultado.split("\n"):
            if "ESSID" in linea:
                ssid = linea.split(":")[1].strip('"')
                if ssid:
                    redes.add(ssid)
    except Exception as e:
        print(f"Error al escanear redes: {e}")
    return redes

def configurar_access_point(ssid, password):
    hostapd_config = f"""
    interface=wlan0
    driver=nl80211
    ssid={ssid}
    hw_mode=g
    channel=6
    macaddr_acl=0
    auth_algs=1
    ignore_broadcast_ssid=0
    wpa=2
    wpa_passphrase={password}
    wpa_key_mgmt=WPA-PSK
    wpa_pairwise=CCMP
    rsn_pairwise=CCMP
    """
    try:
        with open('/etc/hostapd/hostapd.conf', 'w') as file:
            file.write(hostapd_config)
        print("Configuración de hostapd completada.")
    except Exception as e:
        print(f"Error al configurar hostapd: {e}")

    os.system("sudo systemctl restart hostapd")
    print(f"Punto de acceso '{ssid}' configurado y activado.")
    os.system("sudo systemctl restart dnsmasq")
    print("Servidor DHCP iniciado.")

if __name__ == '__main__':
    redes_existentes = escanear_redes()
    while True:
        ssid = input("Ingresa el nombre del punto de acceso SSID: ")
        if ssid in redes_existentes:
            print("Este SSID ya existe, ingresa otro nombre.")
        else:
            break
    password = input("Ingresa la contraseña para la red: ")
    configurar_access_point(ssid, password)
