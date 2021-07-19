import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('device_id', var_type='Device')
dev_var.add('address.0.object_id', var_type='String')
dev_var.add('address.0.type', var_type='String')
dev_var.add('address.0.address', var_type='Composite')
dev_var.add('address.0.network_address', var_type='Composite')
dev_var.add('address.0.network_mask', var_type='Composite')
dev_var.add('address.0.start_address', var_type='Composite')
dev_var.add('address.0.end_address', var_type='Composite')
dev_var.add('address.0.fqdn', var_type='Composite')

context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['device_id']

# extract the database ID
devicelongid = device_id[3:]

# build the Microservice JSON params
#{"Gateway":"0"}
#micro_service_vars_array = {"object_id":object_id}
object_parameters = {}

object_parameters['address'] = {}
for v in context['address']:
  object_parameters['address'][v['object_id']] = v


# call the CREATE for the specified MS for each device
order = Order(devicelongid)
order.command_execute('CREATE', object_parameters)

# convert dict object into json
content = json.loads(order.content)

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

