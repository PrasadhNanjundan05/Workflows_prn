'''
Visit http://[YOUR_MSA_URL]/msa_sdk/ to see what you can import.
'''
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('host', var_type='String')
dev_var.add('username', var_type='String')
dev_var.add('password', var_type='String')
dev_var.add('quickstartDir', var_type='String')



context = Variables.task_call(dev_var)

def test():
    return "Success"

ret = MSA_API.process_content('ENDED', f'Backup successful '+test(), context, True)
print(ret)

