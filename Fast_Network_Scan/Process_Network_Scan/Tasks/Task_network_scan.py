from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
import nmap

dev_var = Variables()
dev_var.add('network', var_type='String')

context = Variables.task_call(dev_var)

nm = nmap.PortScanner()
nm.scan(hosts=context['network'], arguments='-n -sP')
hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
i=0
for host, status, state in hosts_list:
    context['hosts'][i]['host'] = host
    context['hosts'][i]['status'] = status
    context['hosts'][i]['state'] = state
    i += 1

ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
print(ret)

