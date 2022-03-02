from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('test_list.0.select', var_type='Boolean')
dev_var.add('test_list.0.name', var_type='String')

context = Variables.task_call(dev_var)

ret = MSA_API.process_content('ENDED', 'Update OK', context, True)
print(ret)

