#UDP Server - Emilio Conejeros

import socket
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(('localhost', 65432))
    print('Servidor escuchando en localhost:65432')
    
    while True:
        data, client_address = server_socket.recvfrom(1024)
        print('Recibido desde', client_address, ':', data.decode())
        message = 'Hola, cliente. Soy el servidor.'.encode()
        print('Enviando:',message.decode())
        server_socket.sendto(message,client_address)

start_server()
