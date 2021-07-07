from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
from msa_sdk.conf_profile import ConfProfile
import re
import json
import time

dev_var = Variables()
dev_var.add('aws_ip', var_type='IP Address')
dev_var.add('aws_username', var_type='String')
dev_var.add('aws_password', var_type='String')
dev_var.add('aws_hostname', var_type='String')


context = Variables.task_call(dev_var)

msa_object  = MSA_API()

customerId = re.match('^\D+?(\d+?)$',context['UBIQUBEID']).group(1)
prefix = re.match('^(\D{3})?A\d+?$',context['UBIQUBEID']).group(1)

msa_object.path = "/device/v1/customer/{}/device-features".format(customerId)
msa_object._call_get()

device_exists = False
for device in json.loads(msa_object.content):
        if device['externalReference'] == 'AWSDISME':
            context['device_id'] = prefix+str(device['id'])
            device_exists = True

if not device_exists:
    aws_device = Device(customer_id = customerId, 
                        name = 'AWS Discovery ME', 
                        device_external = 'AWSDISME',
                        manufacturer_id = '17010301',
                        password_admin = '',
                        model_id = '17010301',
                        login = context['aws_username'], 
                        password = context['aws_password'], 
                        management_address = context['aws_ip'],
                        management_port = '')

    aws_device.create()
    output = aws_device.read()
    aws_device_info = json.loads(output)


    msa_object.action = 'Update Device Hostname'
    msa_object.path   = "/device/v1/{}/hostname/{}".format(aws_device_info['id'], context['aws_hostname'])
    msa_object._call_put()

    conf_profile = ConfProfile(profile_id=179)
    conf_profile.read()


    conf_profile.attachedManagedEntities = [aws_device_info['id']]
    conf_profile.update()

    aws_device.initial_provisioning()
    while aws_device.provision_status()['status'] == 'RUNNING':
        time.sleep(3)
        
    context['device_id'] = prefix+str(aws_device_info['id'])


ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
print(ret)

