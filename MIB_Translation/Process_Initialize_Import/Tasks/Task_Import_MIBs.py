
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API


dev_var = Variables()
dev_var.add('import_mibs_path', var_type='String')

context = Variables.task_call(dev_var)
import_mibs_path = context['import_mibs_path']

ret = MSA_API.process_content('ENDED', 'Import OK', context, True)
print(ret)

