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
from Crypto.Random import get_random_bytes

def encrypt(username, password, shared_key):
    data = f"{username}:{password}".encode("utf-8")

    # Generate Initialization Vector (IV)
    iv = get_random_bytes(16)

    # Convert the shared key to bytes
    secret_key = shared_key.encode("utf-8")

    # Create Cipher instance
    cipher = AES.new(secret_key, AES.MODE_CBC, iv)

    # Encrypt the data
    encrypted_bytes = cipher.encrypt(data)

    # Base64 encode the encrypted data
    encrypted_text = base64.b64encode(iv + encrypted_bytes).decode("utf-8")
    return encrypted_text


try:
    encrypted_data = encrypt(context.get("user"), context.get("pass"), context.get("secret_key"))
    context["encrypted_string_for_user"] = encrypted_data
except Exception as e:
    print(e)

ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
util.log_to_process_file(service_id, str(ret), process_id)
print(ret)


