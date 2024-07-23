import tkinter as tk
from tkinter import messagebox, simpledialog
import sqlite3
import pyotp
import qrcode
from PIL import Image, ImageTk
import firebase_admin
from firebase_admin import credentials, auth
import os
from cryptography.fernet import Fernet
import sys

# Configuración de Firebase
cred = credentials.Certificate('path/to/your/firebase-adminsdk.json')
firebase_admin.initialize_app(cred)

# Ruta del archivo de clave
CLAVE_ARCHIVO = "utils/clave.key"

# Generar una clave y guardarla en un archivo para uso futuro
def generar_clave():
    clave = Fernet.generate_key()
    with open("clave.key", "wb") as clave_file:
        clave_file.write(clave)
    print("Clave generada y guardada en clave.key")

def cargar_clave():
    try:
        if os.path.exists("clave.key"):
            with open("clave.key", "rb") as clave_file:
                return clave_file.read()
        else:
            print("Archivo de clave no encontrado. Generando nueva clave...")
            return generar_clave()
    except IOError as e:
        print(f"Error al abrir el archivo de clave: {e}")
        raise

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "generar_clave":
        generar_clave()
    else:
        clave = cargar_clave()
        fernet = Fernet(clave)

# Crear la base de datos
conn = sqlite3.connect('password_manager.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                full_name TEXT,
                nickname TEXT,
                email TEXT,
                phone TEXT,
                password TEXT,
                secret TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                url TEXT,
                username TEXT,
                password TEXT,
                gmail TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id))''')

conn.commit()

# Función para registrar un nuevo usuario
def registrar_usuario():
    full_name = simpledialog.askstring("Registro", "Nombre completo:")
    nickname = simpledialog.askstring("Registro", "Apodo:")
    email = simpledialog.askstring("Registro", "Correo electrónico:")
    phone = simpledialog.askstring("Registro", "Número de teléfono:")
    password = simpledialog.askstring("Registro", "Contraseña:", show='*')

    if not full_name or not nickname or not email or not phone or not password:
        messagebox.showwarning("Advertencia", "Todos los campos son obligatorios")
        return

    secret = pyotp.random_base32()
    c.execute("INSERT INTO users (full_name, nickname, email, phone, password, secret) VALUES (?, ?, ?, ?, ?, ?)", 
              (full_name, nickname, email, phone, password, secret))
    conn.commit()

    otp_uri = pyotp.totp.TOTP(secret).provisioning_uri(name=nickname, issuer_name="PasswordManager")
    qr = qrcode.make(otp_uri)
    qr.save("qrcode.png")

    qr_window = tk.Toplevel(root)
    qr_window.title("QR Code")
    img = Image.open("qrcode.png")
    img = ImageTk.PhotoImage(img)
    panel = tk.Label(qr_window, image=img)
    panel.image = img
    panel.pack()

    messagebox.showinfo("Registro exitoso", "Usuario registrado con éxito. Escanee el código QR con Google Authenticator o Apple.")

# Función para iniciar sesión
def iniciar_sesion():
    email = simpledialog.askstring("Iniciar sesión", "Correo electrónico:")
    password = simpledialog.askstring("Iniciar sesión", "Contraseña:", show='*')

    c.execute("SELECT * FROM users WHERE email=? AND password=?", (email, password))
    user = c.fetchone()
    
    if user:
        user_id = user[0]
        phone = user[4]
        secret = user[6]

        totp = pyotp.TOTP(secret)
        otp = simpledialog.askstring("2FA", "Ingrese el código de autenticación:")
        
        if totp.verify(otp):
            messagebox.showinfo("Inicio de sesión exitoso", "Bienvenido!")
            abrir_gestor_contraseñas(user_id)
        else:
            messagebox.showwarning("Error", "Código de autenticación incorrecto")
    else:
        messagebox.showwarning("Error", "Correo electrónico o contraseña incorrectos")

# Función para abrir el gestor de contraseñas
def abrir_gestor_contraseñas(user_id):
    gestor = tk.Toplevel(root)
    gestor.title("Gestor de Contraseñas")

    # Columnas: URL, Nombre de usuario, Contraseña, Gmail
    tk.Label(gestor, text="URL").grid(row=0, column=0, padx=10, pady=5, sticky="w")
    tk.Label(gestor, text="Nombre de usuario").grid(row=0, column=1, padx=10, pady=5, sticky="w")
    tk.Label(gestor, text="Contraseña").grid(row=0, column=2, padx=10, pady=5, sticky="w")
    tk.Label(gestor, text="Gmail").grid(row=0, column=3, padx=10, pady=5, sticky="w")

    # Función para agregar una nueva contraseña
    def agregar_contraseña():
        url = simpledialog.askstring("Agregar contraseña", "URL:")
        username = simpledialog.askstring("Agregar contraseña", "Nombre de usuario:")
        password = simpledialog.askstring("Agregar contraseña", "Contraseña:", show='*')
        gmail = simpledialog.askstring("Agregar contraseña", "Gmail (opcional):")

        if not url or not username or not password:
            messagebox.showwarning("Advertencia", "URL, nombre de usuario y contraseña son obligatorios")
            return

        encrypted_password = fernet.encrypt(password.encode()).decode()

        c.execute("INSERT INTO passwords (user_id, url, username, password, gmail) VALUES (?, ?, ?, ?, ?)",
                  (user_id, url, username, encrypted_password, gmail))
        conn.commit()
        actualizar_lista_contraseñas()

    # Función para actualizar la lista de contraseñas
    def actualizar_lista_contraseñas():
        for widget in gestor.grid_slaves():
            if int(widget.grid_info()["row"]) > 0:
                widget.grid_forget()

        c.execute("SELECT * FROM passwords WHERE user_id=?", (user_id,))
        passwords = c.fetchall()
        
        for idx, pwd in enumerate(passwords):
            tk.Label(gestor, text=pwd[2]).grid(row=idx+1, column=0, padx=10, pady=5, sticky="w")
            tk.Label(gestor, text=pwd[3]).grid(row=idx+1, column=1, padx=10, pady=5, sticky="w")
            tk.Label(gestor, text="******").grid(row=idx+1, column=2, padx=10, pady=5, sticky="w")
            tk.Label(gestor, text=pwd[5]).grid(row=idx+1, column=3, padx=10, pady=5, sticky="w")
            tk.Button(gestor, text="Ver", command=lambda p=pwd: ver_contraseña(p)).grid(row=idx+1, column=4, padx=10, pady=5)

    # Función para ver la contraseña
    def ver_contraseña(pwd):
        decrypted_password = fernet.decrypt(pwd[4].encode()).decode()
        messagebox.showinfo("Contraseña", f"Contraseña: {decrypted_password}")

    tk.Button(gestor, text="Agregar contraseña", command=agregar_contraseña).grid(row=1, column=4, padx=10, pady=10)
    actualizar_lista_contraseñas()

# Configuración de la interfaz principal
root = tk.Tk()
root.title("Gestor de Contraseñas")

main_frame = tk.Frame(root, bg="#f5f5f5")
main_frame.pack(fill="both", expand=True, padx=20, pady=20)

tk.Label(main_frame, text="Asegúrate de obtener tus credenciales de Firebase desde el sitio oficial:").pack(pady=(0, 10))
tk.Label(main_frame, text="https://firebase.google.com/").pack(pady=(0, 20))

tk.Button(main_frame, text="Registrar", command=registrar_usuario).pack(pady=10)
tk.Button(main_frame, text="Iniciar sesión", command=iniciar_sesion).pack(pady=10)

root.mainloop()
