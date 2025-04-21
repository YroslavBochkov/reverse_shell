import socket
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv()
HOST = '127.0.0.1'  # Standard loopback interface address (localhost)
PORT = 8888        # Port to listen on (non-privileged ports are > 1023)
KEY = os.getenv("ENCRYPTION_KEY").encode() #  Получаем ключ из .env

f = Fernet(KEY)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    conn, addr = s.accept()
    with conn:
        print('Connected by', addr)
        while True:
            data = conn.recv(1024)
            if not data:
                break
            decrypted_data = f.decrypt(data)
            print('Received:', decrypted_data.decode())
            command = input("> ")
            encrypted_command = f.encrypt(command.encode())
            conn.sendall(encrypted_command)
