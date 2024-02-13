import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")

from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import util
import base64
from hashlib import sha256
from hmac import HMAC
from os import urandom
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend


dev_var = Variables()
dev_var.add('user', var_type='String')
dev_var.add('pass', var_type='Password')

context = Variables.task_call(dev_var)

service_id = context['SERVICEINSTANCEID']
process_id = context['PROCESSINSTANCEID']

def pad(data):
    padder = padding.PKCS7(128).padder()
    padded_data = padder.update(data) + padder.finalize()
    return padded_data

def encrypt(username, password, sharedKey):
    data = username + ":" + password
    
    # Generate Initialization Vector (IV)
    iv = urandom(16)  # Random IV
    
    # Derive key from sharedKey using HMAC
    key = HMAC(sharedKey.encode('utf-8'), iv, sha256).digest()
    
    # Encrypt the data
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(pad(data.encode('utf-8'))) + encryptor.finalize()
    
    # Combine IV and encrypted data and Base64 encode
    encrypted_bytes = iv + encrypted_data
    return base64.b64encode(encrypted_bytes).decode('utf-8')



try:
    encrypted_data = encrypt(context.get("user"), context.get("pass"), context.get("secret_key"))
    context["encrypted_string_for_user"] = encrypted_data
except Exception as e:
    print(e)

ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
util.log_to_process_file(service_id, str(ret), process_id)
print(ret)


