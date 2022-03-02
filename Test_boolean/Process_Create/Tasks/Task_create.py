from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()

context = Variables.task_call(dev_var)
test_list = []
test_list.append({'select': False, 'name': 'A'})
test_list.append({'select': False, 'name': 'B'})
test_list.append({'select': False, 'name': 'C'})

context['test_list'] = test_list

ret = MSA_API.process_content('ENDED', 'Create OK', context, True)
print(ret)

