import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk.orchestration import Orchestration

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('device_id', var_type='Device')

context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['device_id']

# extract the database ID
devicelongid = device_id[3:]

orch = Orchestration(context['UBIQUBEID'])
ret = orch.get_service_status_by_id(context['SERVICEINSTANCEID'])
context['service_instances'] = ret

# build the Microservice JSON params
#{"Gateway":"0"}
#micro_service_vars_array = {"object_id":object_id}
object_parameters = {}

object_parameters['Failover'] = '0';


# call the CREATE for the specified MS for each device
order = Order(devicelongid)
order.command_execute('IMPORT', object_parameters)

# convert dict object into json
content = json.loads(order.content)

# check if the response is OK
if order.response.ok:
    if content['message'] == '{}':
        # the route does not exist
        context['state'] = 'SIX2 is active'
    else:
        context['state'] = 'SIX1 is active'
    
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

