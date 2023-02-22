from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()

context = Variables.task_call(dev_var)

import time
time.sleep(10)

ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
print(ret)

