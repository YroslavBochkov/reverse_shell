from cryptography.fernet import Fernet

key = Fernet.generate_key()
print(key) # Сохраните этот ключ в безопасном месте!
