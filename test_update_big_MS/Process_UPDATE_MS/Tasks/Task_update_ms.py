import json

from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
from msa_sdk.order import Order

 
dev_var = Variables()
#dev_var.add('var_name', var_type='String')
dev_var.add('var_name2', var_type='Integer')

context = Variables.task_call(dev_var)

# build the Microservice JSON params
# object_parameters = {}
# object_parameters['VNI_POOL'] = {}
# object_parameters['VNI_POOL'][object_id] = {}
# object_parameters['VNI_POOL'][object_id]['object_id']                = object_id
# object_parameters['VNI_POOL'][object_id]['name']                     = context['name']
# object_parameters['VNI_POOL'][object_id]['SERVICEINSTANCEREFERENCE'] = context['SERVICEINSTANCEREFERENCE']
# object_parameters['VNI_POOL'][object_id]['SERVICEINSTANCEID']        = context['SERVICEINSTANCEID']
# object_parameters['VNI_POOL'][object_id]['description']              = context['description']
# object_parameters['VNI_POOL'][object_id]['pool']                     = context['pool']
# object_parameters['VNI_POOL'][object_id]['vnisInUse']               = context['vnisInUse']


object_parameters = json.loads(context['params_string']) 
object_id = "90d11a7c-c46e-41ed-95b9-3a32463ce0d3"
object_parameters['VNI_POOL']["90d11a7c-c46e-41ed-95b9-3a32463ce044"] = object_parameters['VNI_POOL'][object_id]
object_parameters['VNI_POOL']["90d11a7c-c46e-41ed-95b9-3a32463ce055"] = object_parameters['VNI_POOL'][object_id]
object_parameters['VNI_POOL']["90d11a7c-c46e-41ed-95b9-3a32463ce066"] = object_parameters['VNI_POOL'][object_id]

#for i in range(100, 200)::
#  new_object_id = '"90d11a7c-c46e-41ed-95b9-3a32463ce'+str(i)	
#  object_parameters['VNI_POOL'][new_object_id] = object_parameters['VNI_POOL'][object_id]



devicelongid = 162
command = 'UPDATE'
order    = Order(devicelongid)
  
# call the UPDATE for the specified MS for each device
# send_continuous_request_on_MS('UPDATE', devicelongid, 'VNI_POOL', object_parameters)
order.command_call(command, 2, object_parameters)

MSA_API.task_success('DONE', context, True)

 

