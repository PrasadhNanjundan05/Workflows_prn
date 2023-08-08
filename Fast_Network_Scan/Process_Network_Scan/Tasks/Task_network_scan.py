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
context['hosts'] = list()

Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'],
                     context['TASKID'], context['EXECNUMBER'])
status_message = ''
i = 0
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
        host_info = dict()
        host_info['ip_address'] = result.group(1)
        host_info['selected'] = True
        host_info['vendor'] = None
        host_info['model'] = None
        context['hosts'].append(host_info)
        update_message = True
        i += 1
    else:
        result = re.match('^Ping\sScan\sTiming:\s(.*)', line.decode())
        if result:
            status_message = result.group(1)
            update_message = True
    if update_message:
        update_info(i, status_message) 

ret = MSA_API.process_content('ENDED', 'Task OK : '+str(i)+' hosts found', context, True)
print(ret)