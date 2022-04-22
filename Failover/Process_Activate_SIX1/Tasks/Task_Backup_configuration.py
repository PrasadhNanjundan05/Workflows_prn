from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.conf_backup import ConfBackup
from time import sleep

dev_var = Variables()

context = Variables.task_call(dev_var)

device_id = context['device_id']
devicelongid = device_id[3:]

conf_backup = ConfBackup()
conf_backup.backup(devicelongid)
result = 'RUNNING'
retry = 100
while result == 'RUNNING' and retry > 0:
    sleep(1)
    result = conf_backup.backup_status(devicelongid)
    retry--

if result == 'ENDED':
    ret = MSA_API.process_content('ENDED', 'Backup done', context, True)
else:
    ret = MSA_API.process_content('FAILED', 'Backup failed', context, True)
print(ret)

