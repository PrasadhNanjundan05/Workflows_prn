from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('array.0.select', var_type='Boolean')

context = Variables.task_call(dev_var)

ret = MSA_API.process_content('ENDED', 'Update OK', context, True)
print(ret)

