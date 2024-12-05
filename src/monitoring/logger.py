# Registro de eventos
import logging
import os

class Logger:
    def __init__(self, log_file='app.log'):
        # Se asegura de que la carpeta "logs" exista
        log_dir = os.path.join(os.path.dirname(__file__), "logs")
        os.makedirs(log_dir, exist_ok=True)

        # Ruta completa del archivo de log
        log_path = os.path.join(log_dir, log_file)

        # Configuración del logger
        self.logger = logging.getLogger('NetworkLogger')
        self.logger.setLevel(logging.DEBUG)

        # Configuración del archivo de log
        file_handler = logging.FileHandler(log_path)
        file_handler.setLevel(logging.DEBUG)

        # Configuración del formato
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)

        # Agregar manejadores al logger
        self.logger.addHandler(file_handler)

    def log_info(self, message):
        """Registra un mensaje de nivel INFO."""
        self.logger.info(message)

    def log_warning(self, message):
        """Registra un mensaje de nivel WARNING."""
        self.logger.warning(message)

    def log_error(self, message):
        """Registra un mensaje de nivel ERROR."""
        self.logger.error(message)


if __name__ == "__main__":
    # Ejemplo de uso
    log = Logger("test.log")
    log.log_info("Este es un mensaje informativo")
    log.log_warning("Este es un mensaje de advertencia")
    log.log_error("Este es un mensaje de error")
