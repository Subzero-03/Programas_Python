from flask import Flask, request, jsonify
import sqlite3
import pyotp

app = Flask(__name__)

# Crear la base de datos y las tablas necesarias
conn = sqlite3.connect('password_manager.db')
c = conn.cursor()

c.execute('''CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY,
                full_name TEXT,
                nickname TEXT,
                email TEXT,
                phone TEXT,
                password TEXT,
                secret TEXT,
                nexmo_api_key TEXT,
                nexmo_api_secret TEXT)''')

c.execute('''CREATE TABLE IF NOT EXISTS passwords (
                id INTEGER PRIMARY KEY,
                user_id INTEGER,
                url TEXT,
                username TEXT,
                password TEXT,
                gmail TEXT,
                FOREIGN KEY(user_id) REFERENCES users(id))''')

conn.commit()


@app.route('/generate_qr', methods=['POST'])
def generate_qr():
    data = request.json
    nickname = data['nickname']
    secret = pyotp.random_base32()
    c.execute("UPDATE users SET secret=? WHERE nickname=?", (secret, nickname))
    conn.commit()

    otp_uri = pyotp.totp.TOTP(secret).provisioning_uri(name=nickname, issuer_name="PasswordManager")
    return jsonify({'otp_uri': otp_uri})

if __name__ == '__main__':
    app.run(port=5000)
