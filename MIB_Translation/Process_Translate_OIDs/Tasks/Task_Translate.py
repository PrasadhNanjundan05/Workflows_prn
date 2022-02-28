import os

from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

'''
List all the parameters required by the task

You can use var_name convention for your variables
They will display automaticaly as "Var Name"
The allowed types are:
  'String', 'Boolean', 'Integer', 'Password', 'IpAddress',
  'IpMask', 'Ipv6Address', 'Composite', 'OBMFRef', 'Device'

 Add as many variables as needed
'''
dev_var = Variables()
dev_var.add('imported_oids.0.oid_name', var_type='String')
dev_var.add('imported_oids.0.oid', var_type='String')
dev_var.add('imported_oids.0.selected', var_type='String')

'''
context => Service Context variable per Service Instance
All the user-inputs of Tasks are automatically stored in context
Also, any new variables should be stored in context which are used across Service Instance
The variables stored in context can be used across all the Tasks and Processes of a particular Service
Update context array [add/update/delete variables] as per requirement

ENTER YOUR CODE HERE
'''
context = Variables.task_call(dev_var)

'''
Store selected oid in a file
'''
dst_path = '/opt/fmc_repository/Datafiles/MIBs_translation/'
file_name = 'oid_translated'
tmp_file = dst_path + '/' + file_name + '.tmp'
dst_file = dst_path + '/' + file_name + '.txt'

oid_str = ''
imported_oid_list = context['imported_oids']


for oid_obj in imported_oid_list:
    if 'selected' in oid_obj:
        if oid_obj['selected']:
            oid_str += '"{}" "{}"\n'.format(oid_obj['oid_name'], oid_obj['oid'])

with open(tmp_file, 'w') as f:
    f.write(oid_str)

os.rename(tmp_file, dst_file)

'''
Format of the Task response :
JSON format : {"wo_status":"status","wo_comment":"comment","wo_newparams":{json_body}}
wo_status : ENDED [Green color] or FAILED [Red color] or WARNING [Orange color]
			-> While the Task is Running [means no response returned yet], task status is RUNNING [Blue color]
         -> When status is returned as FAILED, the Orchestration Engine stops the Process Execution from this Task
wo_comment : Appropriate Comment to display as per the success/failure of the Task
wo_newparams : json_body parameters returned from this Task

Function process_content() takes care of Creating a Json response from inputs
This function definiton can be found at : http://[YOUR_MSA_URL]/msa_sdk/msa_api.html#msa_sdk.msa_api.MSA_API.process_content
NOTE : For 'wo_newparams', always pass "context" [whether wo_status is ENDED/FAILED/WARNING to preserve it across Service Instance]
    -> Last argument "true" mentions whether the json_response to be Logged in the logfile : /opt/jboss/latest/logs/process.log
    -> If not passed, it's "false"

The response "ret" should be echoed from the Task "print(ret)" which is read by Orchestration Engine
In case of FAILURE/WARNING, the Task can be Terminated by calling "exit" as per Logic
'''
ret = MSA_API.process_content('ENDED', f'Task OK\nfile created {dst_file}', context, True)
print(ret)

