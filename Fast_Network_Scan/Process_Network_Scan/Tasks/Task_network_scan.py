from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
import nmap

dev_var = Variables()
dev_var.add('network', var_type='String')

context = Variables.task_call(dev_var)

nm = nmap.PortScanner()
nm.scan(hosts=context['network'], arguments='-n -sP')
hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]
i = 0
for host, status in hosts_list:
    if i == 0
    	context['hosts'] = dict()
        context['hosts'][i] = dict()
    context['hosts'][i]['host'] = host
    context['hosts'][i]['status'] = status
    i += 2

ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
print(ret)

