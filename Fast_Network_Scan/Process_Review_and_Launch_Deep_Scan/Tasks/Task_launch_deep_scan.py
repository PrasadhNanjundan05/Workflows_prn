from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.orchestration import Orchestration
from msa_sdk import util
import json
import time

dev_var = Variables()
dev_var.add('hosts.0.ip_address', var_type='Ip Address')
dev_var.add('hosts.0.selected', var_type='Boolean')
dev_var.add('snmp_communities.0.name', var_type='String')
context = Variables.task_call(dev_var)

Orchestration = Orchestration(context['UBIQUBEID'])

hosts = context['hosts']
communities = context['snmp_communities']

selected_hosts = list()

for host in hosts:
    selected = bool(host['selected'])
    if selected:
        selected_host = dict()
        selected_host['ip_address'] = host['ip_address']
        selected_hosts.append(selected_host)
        
hosts_per_wf = []
process_ids = dict()

for host in selected_hosts:
    hosts_per = dict()
    hosts_per['ip_address'] = host['ip_address']
    hosts_per_wf.append(hosts_per)
    if len(hosts_per_wf) == 2:
        data = dict()
        data['hosts'] = dict()
        data['hosts'] = hosts_per_wf
        data['snmp_communities'] = communities
        serviceId, processId = Orchestration.execute_service_process('Process/workflows/Deep_Network_Scan/Deep_Network_Scan', 'Process/workflows/Deep_Network_Scan/Process_Deep_Network_Scan', data)
        if processId and serviceId is not None:
            process_info = dict()
            process_info[processId] = serviceId
            process_ids.update(process_info);
        hosts_per_wf = []

while bool(process_ids):
    for k, v in list(process_ids.items()):
        process_status = Orchestration.get_process_status_by_id(k)
        if process_status == 'RUNNING':
            time.sleep(5)
        elif process_status == 'ENDED':
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

