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
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad

def encrypt(username, password, shared_key):
    data = f"{username}:{password}"
    iv = b'\x00' * 16  # Initialize IV (16 bytes of zeros)
    secret_key = shared_key.encode('utf-8')
    
    # Create AES cipher object
    cipher = AES.new(secret_key, AES.MODE_CBC, iv)
    
    # Encrypt the data
    encrypted_bytes = cipher.encrypt(pad(data.encode('utf-8'), AES.block_size))
    
    # Encode the encrypted bytes to base64
    encrypted_data = base64.b64encode(encrypted_bytes).decode('utf-8')
    return encrypted_data


try:
    encrypted_data = encrypt(context.get("user"), context.get("pass"), context.get("secret_key"))
    context["encrypted_string_for_user"] = encrypted_data
except Exception as e:
    print(e)

ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
util.log_to_process_file(service_id, str(ret), process_id)
print(ret)


