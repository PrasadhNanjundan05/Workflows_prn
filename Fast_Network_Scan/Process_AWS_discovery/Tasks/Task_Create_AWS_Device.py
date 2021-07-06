from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
import re

dev_var = Variables()
dev_var.add('aws_ip', var_type='IP Address')
dev_var.add('username', var_type='String')
dev_var.add('password', var_type='String')

context = Variables.task_call(dev_var)

aws_device = Device(customer_id = re.match('^\D+?(\d+?)$',context['UBIQUBEID']).group(1), 
                        name = 'AWS Discovery ME', 
                        device_external = '',
                        manufacturer_id = '17010301',
                        password_admin = '',
                        model_id = '17010301',
                        login = context['username'], 
                        password = context['password'], 
                        management_address = context['aws_ip'],
                        management_port = '')

aws_device.create()
output = aws_device.read()
aws_device_info = json.loads(output)

conf_profile = ConfProfile(profileId=9096)
conf_profile.read()


conf_profile.attachedManagedEntities = [aws_device_info['id']]
conf_profile.update()


ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
print(ret)

