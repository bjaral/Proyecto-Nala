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
        invalid_chars = "!#$%&/()=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
        
        # Validar caracteres inválidos en el JSON completo (claves y valores como strings)
        for key, value in data.items():
            if any(char in invalid_chars for char in str(key)):
                print(f"Clave inválida detectada en los datos de {ip}: {key}")
                self.block_user(ip)
                return False
            
            # Si el valor es un dict o lista, validar recursivamente
            if isinstance(value, dict):
                if not self.validate_data(value, ip):
                    return False
            
            elif isinstance(value, list):
                for item in value:
                    if isinstance(item, (dict, list)):
                        if not self.validate_data(item, ip):
                            return False
                    elif any(char in invalid_chars for char in str(item)):
                        print(f"Valor inválido detectado en los datos de {ip}: {item}")
                        self.block_user(ip)
                        return False
            
            # Validación de los valores numéricos según los límites
            elif key in ["Acc_X", "Acc_Y", "Acc_Z"]:
                if not isinstance(value, (int, float)) or not (-16.0 <= value <= 16.0):
                    print(f"Valor fuera de rango para {key} en {ip}: {value}")
                    self.block_user(ip)
                    return False
            
            elif key in ["Rgy_X", "Rgy_Y", "Rgy_Z"]:
                if not isinstance(value, (int, float)) or not (-1000 <= value <= 1000):
                    print(f"Valor fuera de rango para {key} en {ip}: {value}")
                    self.block_user(ip)
                    return False
                        
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
                return False
            
            else:
                print(f'Paquete recibido exitosamente por {ip}')
                return True
        
        except json.JSONDecodeError:
            print(f'Formato inválido')
            self.block_user(ip)
            print('Usuario bloqueado')
            return False
        
    