# Captura tráfico con wireshark
import pyshark
from logger import Logger

class NetworkMonitor:
    def __init__(self, interface='eth0', log_file='network_events.log'):
        self.interface = interface
        self.logger = Logger(log_file)

    def capture_packets(self):
        """Captura y analiza paquetes de la interfaz en tiempo real."""
        try:
            self.logger.log_info(f"Iniciando monitoreo en la interfaz {self.interface}")
            capture = pyshark.LiveCapture(interface=self.interface)

            for packet in capture.sniff_continuously():
                self.process_packet(packet)
        except Exception as e:
            self.logger.log_error(f"Error durante la captura de paquetes: {e}")

    def process_packet(self, packet):
        """Procesa cada paquete capturado y lo registra."""
        try:
            packet_info = {
                'time': packet.sniff_time,
                'protocol': packet.highest_layer,
                'source': packet.ip.src if hasattr(packet, 'ip') else 'Desconocido',
                'destination': packet.ip.dst if hasattr(packet, 'ip') else 'Desconocido',
                'length': packet.length,
            }

            log_message = (f"Paquete capturado: Protocolo={packet_info['protocol']}, "
                           f"Origen={packet_info['source']}, Destino={packet_info['destination']}, "
                           f"Longitud={packet_info['length']}")
            self.logger.log_info(log_message)
        except AttributeError:
            self.logger.log_warning("Paquete no compatible o información incompleta")
        except Exception as e:
            self.logger.log_error(f"Error procesando el paquete: {e}")


if __name__ == "__main__":
    monitor = NetworkMonitor(interface='eth0')  # Cambia 'eth0' por la interfaz de tu Raspberry Pi
    monitor.capture_packets()
