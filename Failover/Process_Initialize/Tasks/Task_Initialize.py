from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('device_id', var_type='Device')
dev_var.add('Failover.object_id', var_type='String')

context = Variables.task_call(dev_var)
context['Failover'] = []
context['Failover']['object_id'] = 'ip'

ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
print(ret)
