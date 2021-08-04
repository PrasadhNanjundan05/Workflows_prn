from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.orchestration import Orchestration
from msa_sdk import util
import json
import time
import math

dev_var = Variables()
dev_var.add('hosts.0.ip_address', var_type='Ip Address')
dev_var.add('hosts.0.selected', var_type='Boolean')
dev_var.add('restrict_hosts_no', var_type='Integer')
dev_var.add('snmp_communities.0.name', var_type='String')
context = Variables.task_call(dev_var)

Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'],context['TASKID'], context['EXECNUMBER'])
communities = context.get('snmp_communities', {})

def divide_chunks(l, n):
    for i in range(0, len(l), n): 
        yield l[i:i + n]

restrict_no = context.get('restrict_hosts_no', 0)
if restrict_no != 0:
    context['hosts'] = context['hosts'][0:int(restrict_no)]
    
context['hosts'] = list(filter(lambda var: var['selected'] == True, context['hosts']))

hosts_per_wf = []
process_ids = dict()

can_launch_seq_wf_nos = 30

hosts_size = len(context['hosts'])
if hosts_size > can_launch_seq_wf_nos:
    hosts_no_per_wf = math.ceil(hosts_size/can_launch_seq_wf_nos)
else:
    hosts_no_per_wf = 1
    

hosts_per_wf = list(divide_chunks(context['hosts'], hosts_no_per_wf))

for hosts in hosts_per_wf:
    data = dict()
    data['hosts'] = hosts
    data['snmp_communities'] = communities
    serviceId, processId = Orchestration.execute_service_process('Process/workflows/Deep_Network_Scan/Deep_Network_Scan', 'Process/workflows/Deep_Network_Scan/Process_Deep_Network_Scan', data)
    if processId and serviceId is not None:
        process_info = dict()
        process_info[processId] = serviceId
        process_ids.update(process_info);

x = 0
while bool(process_ids):
    for k, v in list(process_ids.items()):
        process_status = Orchestration.get_process_status_by_id(k)
        if process_status == 'RUNNING':
            time.sleep(1)
        elif process_status == 'ENDED':
            x += hosts_no_per_wf
            percentage_complete = round(x/hosts_size*100)
            message = str(percentage_complete) + " % completed"
            Orchestration.update_asynchronous_task_details(*async_update_list, message)
            process_ids.pop(k)
            Orchestration.get_service_variables(v)
            hosts = list(filter(lambda var: var['name'] == 'hosts', json.loads(Orchestration.content)))
            hosts = list(hosts[0]['value'].values())
            for host in hosts:
                updated_host = dict()
                updated_host['ip_address'] = host['ip_address']
                updated_host['selected'] = True
                updated_host['vendor'] = host['vendor']
                updated_host['model'] = host['model']
                context['hosts'] = list(map(lambda x: updated_host if x['ip_address'] == host['ip_address'] else x, context['hosts']))
        elif process_status == 'FAIL':
            process_ids.pop(k)
        else:
            continue


ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
print(ret)
