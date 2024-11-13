import socket
import json
import os

#lista de bloqueos
block=set()

def verificar_integridad(message):
    try:
        json.loads(message)
        return True
    except ValueError:
        return False
    
def bloquear_ip(client_ip):
    if client_ip not in block:
        os.system(f"sudo iptables -A INPUT -s {client_ip} -j DROP")
        block.add(client_ip)
        print(f"IP {client_ip} bloqueada a nivel de sistema con iptables.")

def desasociar_dispositivo(mac_address):
    os.system(f"sudo hostapd_cli deathenticate {mac_address}")
    print(f"Dispositivo con MAC {mac_address} desasociado usando hostapd_cli.")

def start_server():

    puerto=65432
    host='localhost'

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, puerto))
    server_socket.listen()

    print(f'Servidor escuchando en {host}:{puerto}')

    while True:
        connection, client_address = server_socket.accept()
        client_ip=client_address[0]

        if client_ip in block:
            print(f"Conexión rechazada de {client_ip}, está en la lista de bloqueo")
            connection.close()
            continue

        try:
            print('Conexión desde', client_address)

            while True:
                data = connection.recv(1024)
                if data:
                    message = data.decode()
                    print('Recibido:', message)
                    
                    if not verificar_integridad(message):
                        print(f"Mensaje corrupto o malicioso detectado de {client_ip}.")
                        bloquear_ip(client_ip)
                        connection.close()
                        break

                    response=message
                    connection.sendall(response.encode())

                else:
                    break
        finally:
            connection.close()

if __name__ == '__main__':
    start_server()