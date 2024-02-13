import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")

from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import util
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import hashlib
import base64


dev_var = Variables()
dev_var.add('user', var_type='String')
dev_var.add('pass', var_type='Password')

context = Variables.task_call(dev_var)

service_id = context['SERVICEINSTANCEID']
process_id = context['PROCESSINSTANCEID']

def encrypt(username, password, shared_key):
    data = f"{username}:{password}".encode("utf-8")

    # Generate Initialization Vector (IV)
    iv = b'\x00' * 16  # For simplicity, all zeros IV is used

    # Ensure the shared key is 32 bytes long (256 bits) for AES-256
    shared_key = hashlib.sha256(shared_key.encode()).digest()

    # Create AES cipher object in CBC mode
    cipher = AES.new(shared_key, AES.MODE_CBC, iv)

    # Pad the data to a multiple of block size
    padded_data = pad(data, AES.block_size)

    # Encrypt the padded data
    encrypted_bytes = cipher.encrypt(padded_data)

    # Base64 encode the encrypted data and IV
    encrypted_data = base64.b64encode(encrypted_bytes).decode("utf-8")
    encrypted_iv = base64.b64encode(iv).decode("utf-8")

    return encrypted_data, encrypted_iv



try:
    encrypted_data = encrypt(context.get("user"), context.get("pass"), context.get("secret_key"))
    context["encrypted_string_for_user"] = encrypted_data
except Exception as e:
    print(e)

ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
util.log_to_process_file(service_id, str(ret), process_id)
print(ret)


