import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")

from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64


dev_var = Variables()
dev_var.add('user', var_type='String')
dev_var.add('pass', var_type='Password')


context = Variables.task_call(dev_var)

def encrypt(username, password, shared_key):
    data = f"{username}:{password}".encode("utf-8")

    # Generate Initialization Vector (IV)
    iv = b'\x00' * 16  # For simplicity, all zeros IV is used

    # Convert the shared key to a SecretKeySpec
    secret_key = base64.b64decode(shared_key)

    # Create Cipher instance
    cipher = Cipher(algorithms.AES(secret_key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Encrypt the data
    encrypted_bytes = encryptor.update(data) + encryptor.finalize()

    # Base64 encode the encrypted data
    return base64.b64encode(encrypted_bytes).decode("utf-8")


try:
    encrypted_data = encrypt(context.get("user"), context.get("pass"), context.get("secret_key"))
    context["encrypted_string_for_user"] = encrypted_data
except Exception as e:
    print(e)


ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
print(ret)

