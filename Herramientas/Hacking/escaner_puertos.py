import socket
import subprocess
import sys
from datetime import datetime
import os

# Limpiar la pantalla según el sistema operativo
if os.name == 'nt':
    subprocess.call('cls', shell=True)  # Para Windows
else:
    subprocess.call('clear', shell=True)  # Para Linux/Unix/Mac

# Solicitar la entrada
remoteServer = input("Ingrese un host remoto para escanear: ")
try:
    remoteServerIP = socket.gethostbyname(remoteServer)
except socket.gaierror:
    print("No se pudo resolver el nombre de host. Saliendo...")
    sys.exit()

# Imprimimos un banner con la información sobre qué host estamos
# a punto de escanear
print("-" * 60)
print("Por favor espere, escaneando el host remoto", remoteServerIP)
print("-" * 60)

# Verificamos a qué hora comenzó el escaneo
t1 = datetime.now()

try:
    for port in range(1, 1025):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex((remoteServerIP, port))

        if result == 0:
            print("Port {}: Open".format(port))
        sock.close()  # Cerrar el socket correctamente
except KeyboardInterrupt:
    print("\nUsted presionó Ctrl + C")
    sys.exit()
except socket.gaierror:
    print("\nNo se pudo resolver el nombre de host. Saliendo...")
    sys.exit()
except socket.error:
    print("\nNo se pudo conectar al servidor. Saliendo...")
    sys.exit()

# Comprobando la hora de nuevo
t2 = datetime.now()

# Calcular la diferencia de tiempo
total = t2 - t1

# Imprimir la información en la pantalla
print("Escaneo completo en: ", total)
