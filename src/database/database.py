import json
import psycopg2

#sudo apt update
#sudo apt install python3-psycopg2


# Conexión a la base de datos PostgreSQL
def conectar_postgres():

    try:
        # Cambia estos valores según tu configuración
        conexion = psycopg2.connect(
            host="localhost",
            database="postgres",
            user="postgres",
            password="tu_contraseña"
        )
        conexion.autocommit = True
        return conexion
    
    except Exception as e:
        print(f"Error al conectar a PostgreSQL: {e}")
        return None
    
# Crear la base de datos
def crear_base_de_datos(cursor, nombre_bd):

    try:
        cursor.execute(f"CREATE DATABASE {nombre_bd}")
        print(f"Base de datos '{nombre_bd}' creada exitosamente.")

    except Exception as e:
        print(f"Error al crear la base de datos: {e}")

# Crear las tablas
def crear_tablas(cursor):

    try:
        # Tabla log
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS log (
            id_device INT PRIMARY KEY,
            status_report INT,
            time_server TIMESTAMP
        );
        """)
        
        # Tabla data_2
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS asignaturas (
            id_device INT PRIMARY KEY,
            racc_x FLOAT,
            racc_y FLOAT,
            racc_z FLOAT,
            rgyr_x FLOAT,
            rgyr_y FLOAT,
            rgyr_z FLOAT,
            time_client DATETIME
        );
        """)

        # Tabla configuration
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS asignaturas (
            id_device INT PRIMARY KEY,
            tcp_port INT,
            udp_port INT,
            host_ip_addr INT,
            ssid VARCHAR(45),
            pass VARCHAR(45)
        );
        """)
        
        print("Tablas creadas exitosamente.")

    except Exception as e:
        print(f"Error al crear las tablas: {e}")

# Insertar datos desde el archivo JSON
def insertar_datos_desde_json(cursor, archivo_json):

    try:
        with open(archivo_json, 'r') as archivo:
            datos = json.load(archivo)
        
        # Insertar log
        for log_entry in datos['log']:
            cursor.execute("""
            INSERT INTO log (id_device, status_report, time_server) 
            VALUES (%s, %s, %s)
            """, (log_entry['id_device'], log_entry['status_report'], log_entry['time_server']))

        # Insertar data_2
        for data_entry in datos['data_2']:
            cursor.execute("""
            INSERT INTO data_2 (id_device, racc_x, racc_y, racc_z, rgyr_x, rgyr_y, rgyr_z, time_client)
            VALUES  (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (data_entry['id_device'], data_entry['racc_x'], data_entry['racc_y'], data_entry['racc_z'],
                   data_entry['rgyr_x'], data_entry['rgyr_y'], data_entry['rgyr_z'], data_entry['time_client'],))

        # Insertar configuration
        for config_entry in datos['configuration']:
            cursor.execute("""
            INSERT INTO configuration (id_device, tcp_port, udp_port, host_ip_addr, ssid, pass)
            VALUES (%s, %s, %s, %s, %s, %s)
            """, (config_entry['id_device'], config_entry['tcp_port'], config_entry['udp_port'],
                  config_entry['host_ip_addr'], config_entry['ssid'], config_entry['pass']))
        
        print("Datos insertados exitosamente desde el archivo JSON.")

    except Exception as e:
        print(f"Error al insertar datos desde JSON: {e}")

def main():

    conexion = conectar_postgres()
    
    if conexion:
        cursor = conexion.cursor()
        
        # Crear base de datos
        crear_base_de_datos(cursor, 'redes_bd')
        
        # Conectarse a la nueva base de datos
        cursor.close()
        conexion.close()
        
        conexion = psycopg2.connect(
            host="localhost",
            database="redes_bd",
            user="postgres",
            password="**nikita"
        )
        conexion.autocommit = True
        cursor = conexion.cursor()
        
        # Crear tablas
        crear_tablas(cursor)

        # Insertar datos desde el archivo JSON
        insertar_datos_desde_json(cursor, 'ejdb.json')
        
        cursor.close()
        conexion.close()

if __name__ == "__main__":
    main()
