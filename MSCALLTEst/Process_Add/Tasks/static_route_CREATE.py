import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('device_id', var_type='Device')
dev_var.add('static_route.0.object_id', var_type='IpAddress')
dev_var.add('static_route.0.subnet', var_type='IpAddress')
dev_var.add('static_route.0.mask', var_type='IpMask')
dev_var.add('static_route.0.gateway', var_type='IpAddress')
dev_var.add('static_route.0.interface', var_type='ObjectRef')
dev_var.add('static_route.0.metric', var_type='Integer')

context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['device_id']

# extract the database ID
devicelongid = device_id[3:]

# build the Microservice JSON params
#{"Gateway":"0"}
#micro_service_vars_array = {"object_id":object_id}
object_parameters = {}

object_parameters['static_route'] = {}
for v in context['static_route']:
  object_parameters['static_route'][v['object_id']] = v


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

