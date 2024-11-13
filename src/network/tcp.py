import socket

def start_server():

    puerto = 65432
    host = "localhost"
    invalid_chars = "!#$%&/()="

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, puerto))
    server_socket.listen()

    print('Servidor escuchando en {host}:{puerto}')

    while True:
        connection, client_address = server_socket.accept()

        try:
            print('Conexión desde', client_address)

            while True:
                data = connection.recv(1024)

                if data:
                    message = data.decode()
                    print('Recibido:', message)
                    
                    if any(char in message for char in invalid_chars):
                        response = "Carácter no válido encontrado en el mensaje."
                    else:
                        response = message  # Echo del mensaje

                    connection.sendall(response.encode())

                else:
                    break

        finally:
            connection.close()

if __name__ == '__main__':
    start_server()