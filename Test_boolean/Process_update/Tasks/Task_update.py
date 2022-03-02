from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('array.0.select', var_type='Boolean')

ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
print(ret)

