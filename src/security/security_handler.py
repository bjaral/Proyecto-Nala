# Los datos cumplen con los protocolos
# Los datos maliciosos son detectados y bloqueados
# Limpieza y validación de datos antes de guardarlos
import json

class SecurityManager:
    def __init__(self):
        self.blocked_users = set()
        
    def block_user(self, ip):
        self.blocked_users.add(ip)
        print(f'Usuario ip = {ip} bloqueado')
        
    def unblock_user(self, ip):
        self.blocked_users.remove(ip)
        print(f'Usuario ip = {ip} desbloqueado')
        
    def validate_data(self, data, ip):
        invalid_chars = "!#$%&/()="
        
        if any(char in data for char in invalid_chars):
            print(f'Dato malicioso enviado desde {ip}')
            self.block_user(ip)
            return False
                        
        else:
            print('Dato válido')
            return True
                        
    def validation_process(self, data, ip):
        # Cuenta con que se va a pasar directamente la ip, client_address[0]
        
        if ip in self.blocked_users:
            print(f'El usuario ip = {ip} está bloqueado, no se puede enviar datos.')
            return False
        
        try:
        
            decoded_data = json.loads(data.decode('utf-8'))
            
            if self.validate_data(decoded_data) == False:
                print(f'Los datos no cumplen con el protocolo, no se puede enviar.')
                self.block_user(ip)
                print('Usuario bloqueado')
                return False
            
            else:
                print(f'Paquete recibido exitosamente por {ip}')
                return True
        
        except json.JSONDecodeError:
            print(f'Formato inválido')
            self.block_user(ip)
            print('Usuario bloqueado')
            return False
        
    