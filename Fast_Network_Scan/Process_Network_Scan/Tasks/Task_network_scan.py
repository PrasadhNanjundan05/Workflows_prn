from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from nmap import nmap

dev_var = Variables()
dev_var.add('network', var_type='String')

context = Variables.task_call(dev_var)

nm = nmap.PortScanner()
nm.scan(hosts=context['network'], arguments='-n -sP')
hosts_list = [(x, nm[x]['status']['state']) for x in nm.all_hosts()]

for host, status in hosts_list:
    context[host] = status

ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
print(ret)

