import os

from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('imported_oids.0.oid_name', var_type='String')
dev_var.add('imported_oids.0.oid', var_type='String')
dev_var.add('imported_oids.0.selected', var_type='Boolean')

context = Variables.task_call(dev_var)

'''
Store selected oid in a file
'''
file_name = context['translated_oid_file_name_without_ext']
tmp_file = dst_path + file_name + '.tmp'
dst_file = dst_path + file_name + '.txt'

oid_str = ''
imported_oid_list = context['imported_oids']

for oid_obj in imported_oid_list:
    if 'selected' in oid_obj:
        if oid_obj['selected']:
            oid_str += '"{}" "{}"\n'.format(oid_obj['oid'], oid_obj['oid_name'])

with open(tmp_file, 'w') as f:
    f.write(oid_str)

os.rename(tmp_file, dst_file)

ret = MSA_API.process_content('ENDED', f'MIB translation completed\nFile created: {dst_file}', context, True)
print(ret)

