from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

dev_var = Variables()
dev_var.add('device_id', var_type='Device')

context = Variables.task_call(dev_var)

device_id = context['device_id']
devicelongid = device_id[3:]

order = Order(devicelongid)

ret = MSA_API.process_content('ENDED', 'STATUS: OK', context, True)

print(ret)

