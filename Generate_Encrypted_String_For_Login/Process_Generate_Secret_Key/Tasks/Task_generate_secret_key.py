from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64

dev_var = Variables()



context = Variables.task_call(dev_var)

key = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,
        salt=b'salt_',
        iterations=100000,
        backend=default_backend()
    ).derive(b"password")

context["secret_key"] = base64.b64encode(key).decode("utf-8")



ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
print(ret)

