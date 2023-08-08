from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

dev_var = Variables()
context = Variables.task_call()

object_id = context['object_id']

lab_linux_ms_02 = {"lab_linux_ms_02":{object_id:{"object_id":object_id}}}

device_id = context['device']
devicelongid = device_id[3:]

order = Order(devicelongid)
order.command_execute('DELETE', lab_linux_ms_02)

ret = MSA_API.process_content('ENDED', f'INSTANCE REMOVED, \
                           	IPTABLES RESTORED.', context, True)

print(ret)