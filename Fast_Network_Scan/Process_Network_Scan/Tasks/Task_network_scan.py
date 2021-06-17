from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.orchestration import Orchestration
import subprocess
import re
import time

dev_var = Variables()
dev_var.add('network', var_type='String')

context = Variables.task_call(dev_var)
network = context['network']
context['hosts'] = dict()

Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])
status_message = ''
i = 0
# throw message
def update_info(no_host_found: int, status_message: str):
    message = "no of host found: "+ str(no_host_found) +" "
    if status_message:
        message += status_message
    Orchestration.update_asynchronous_task_details(*async_update_list, message)
    
update_info(i, status_message)

process = subprocess.Popen(['nmap', '-n', '-sn', '-vvv', network], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
for line in process.stdout:
    update_message = False
    result = re.match('^Nmap\sscan\sreport\sfor\s(\S+)$', line.decode())
    if result:
        context['hosts'][i] = dict()
        context['hosts'][i]['ip_address'] = result.group(1)
        context['hosts'][i]['selected'] = False
        update_message = True
        i += 1 
    else:
        result = re.match('^Ping\sScan\sTiming:\s(.*)', line.decode())
        if result:
            status_message = result.group(1)
            update_message = True
    if update_message:
        update_info(i, status_message) 

time.sleep(1)        
update_info(i, status_message)
time.sleep(1)
            

ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
print(ret)