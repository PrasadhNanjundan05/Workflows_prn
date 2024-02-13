import sys
import warnings

if not sys.warnoptions:
    warnings.simplefilter("ignore")

from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk import util
import os
import base64


dev_var = Variables()



context = Variables.task_call(dev_var)

service_id = context['SERVICEINSTANCEID']
process_id = context['PROCESSINSTANCEID']

key = os.urandom(24)

context["secret_key"] = base64.b64encode(key).decode('utf-8')



ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
util.log_to_process_file(service_id, str(ret), process_id)
print(ret)

