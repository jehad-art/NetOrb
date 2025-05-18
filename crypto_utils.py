from cryptography.fernet import Fernet
import os

# We Set this key securely in env var for production
SECRET_KEY = os.getenv("FERNET_KEY") or Fernet.generate_key()
fernet = Fernet(SECRET_KEY)

def encrypt_credentials(data: dict) -> dict:
    return {k: fernet.encrypt(v.encode()).decode() for k, v in data.items() if v}

def decrypt_credentials(data: dict) -> dict:
    return {k: fernet.decrypt(v.encode()).decode() for k, v in data.items() if v}
