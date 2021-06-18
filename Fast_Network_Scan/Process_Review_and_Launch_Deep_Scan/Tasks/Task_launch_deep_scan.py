from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.orchestration import Orchestration
from msa_sdk import util
import json

dev_var = Variables()
dev_var.add('hostsk.0.ip_address', var_type='Ip Address')
dev_var.add('hostsk.0.selected', var_type='Boolean')
dev_var.add('snmp_communities.0.name', var_type='String')
context = Variables.task_call(dev_var)

Orchestration = Orchestration(context['UBIQUBEID'])

hosts = context['hostsk']
communities = context['snmp_communities']

selected_hosts = dict()
i = 0
for host in hosts:
    selected = bool(host['selected'])
    if selected:
        selected_hosts[i] = dict()
        selected_hosts[i]['ip_address'] = host['ip_address']
        i += 1
        
hosts_per_wf = dict()
j = 0
for key, value in selected_hosts.items():
    hosts_per_wf[j] = dict()
    hosts_per_wf[j]['ip_address'] = value['ip_address']
    j += 1
    if j == 2:
        data = dict()
        data['hosts'] = dict()
        data['hosts'] = hosts_per_wf
        data['snmp_communities'] = communities
        util.log_to_process_file(context['SERVICEINSTANCEID'], json.dumps(data), context['PROCESSINSTANCEID'])
        Orchestration.execute_service('Process/workflows/Deep_Network_Scan/Deep_Network_Scan', 'Process/workflows/Deep_Network_Scan/Process_Deep_Scan', data)
        hosts_per_wf = dict()
        j = 0
    


ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
print(ret)

