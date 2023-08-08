import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk import util

dev_var = Variables()
context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['device_id']

# extract the database ID
devicelongid = device_id[3:]

# build the Microservice JSON params
#{"Gateway":"0"}
#micro_service_vars_array = {"object_id":object_id}
object_parameters = {}

object_parameters['instances'] = '0';
object_parameters['Images'] = '0';

# call the CREATE for the specified MS for each device
order = Order(devicelongid)
order.command_execute('IMPORT', object_parameters)

# convert dict object into json
content = json.loads(order.content)
#util.log_to_process_file(context['SERVICEINSTANCEID'], json.dumps(content['message']), context['PROCESSINSTANCEID'])

message_content = json.loads(content['message'])
instances = message_content['instances']
images = message_content['Images']

for instance in instances:
    instance_info = instances[instance]
    if instance_info['State']['0']['state_name'] == 'running':
        host_info = dict()
        host_info['ip_address'] = instance_info['public_dns_name']
        host_info['selected'] = True
        image_desc = images[instance_info['image_id']]
        host_info['vendor'] = image_desc['image_name']
        host_info['model'] = image_desc['description']
        context['hosts'].append(host_info)
# check if the response is OK
if order.response.ok:
    ret = MSA_API.process_content('ENDED',
                                  f'STATUS: {content["status"]}, \
                                    MESSAGE: successfull',
                                  context, True)
else:
    ret = MSA_API.process_content('FAILED',
                                  f'Import failed \
                                  - {order.content}',
                                  context, True)


print(ret)

