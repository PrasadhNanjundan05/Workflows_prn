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
util.log_to_process_file(context['SERVICEINSTANCEID'], json.dumps(selected_hosts), context['PROCESSINSTANCEID'])



ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
print(ret)

