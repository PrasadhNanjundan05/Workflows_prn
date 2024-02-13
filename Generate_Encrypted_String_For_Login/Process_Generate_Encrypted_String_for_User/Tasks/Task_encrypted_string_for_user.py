import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")

from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import util


dev_var = Variables()
dev_var.add('user', var_type='String')
dev_var.add('pass', var_type='Password')

context = Variables.task_call(dev_var)

service_id = context['SERVICEINSTANCEID']
process_id = context['PROCESSINSTANCEID']

import base64
from hashlib import sha256
from hmac import HMAC
from Crypto.Util.Padding import pad
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

def encrypt(username, password, sharedKey):
    data = username + ":" + password
    
    # Generate Initialization Vector (IV)
    iv = get_random_bytes(16)  # Random IV
    
    # Derive key from sharedKey using HMAC
    key = HMAC(sharedKey.encode('utf-8'), iv, sha256).digest()
    
    # Create AES cipher object
    cipher = AES.new(key, AES.MODE_CBC, iv)
    
    # Encrypt the data
    encrypted_data = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    
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


