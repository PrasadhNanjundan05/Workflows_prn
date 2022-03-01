import os
import re

from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('import_mibs_path', var_type='String')

context = Variables.task_call(dev_var)

import_mibs_path = context['import_mibs_path']

standard_mibs_path = '/usr/share/snmp/mibs'
mibs_path_root_list = [standard_mibs_path, import_mibs_path]
mibs_path_list = {} # use a dictionary to have each path once

extention_mib_file_list = ('.txt')
mibs_name_dict = {}

'''
Get the list of the MIB names and the list of the path where MIBs are located
    Walk through the mib_path_root_list recursively
    For each file having an extension name in extention_mib_file_list
    get the MIB name and save the result in the dictionary mibs_name_dict
    except for standard mibs (standard_mibs_path)
    Path where MIBs are located are stored in the dictionary mibs_path_list
'''
pattern = '^\s*([^\s]+)\s+DEFINITIONS\s+::= BEGIN'
regc = re.compile(pattern)
def build_mib_mapping(mibs_name_dict, dirpath, fname):
    mib_file = dirpath + os.path.sep + fname
    with open(mib_file, 'r') as f:
        for line in f:
            result = regc.search(line)
            if result != None:
                mib_name = result.group(1)
                mibs_name_dict[mib_name] = fname
                break
    return mibs_name_dict

for mib_path in mibs_path_root_list:
    for dirpath, dirs, files in os.walk(mib_path):
        for fname in files:
            if fname.endswith(extention_mib_file_list):
                if mib_path != standard_mibs_path:
                    mibs_name_dict = build_mib_mapping(mibs_name_dict, dirpath, fname)
                if not dirpath in mibs_path_list:
                    mibs_path_list[dirpath] = True

if not mibs_name_dict:
    context['imported_oids'] = []
    context['import_summary'] = 'Total 0'
    ret = MSA_API.process_content('ENDED', 'No MIB to import', context, True)
    print(ret)

'''
Convert mibs_name_dict dictionary to a list to store in the context
'''
mibs_name_list = []
for mib_name in mibs_name_dict.keys():
    mibs_name_list.append({'name': mib_name, 'selected' : False})

context['mibs_name'] = mibs_name_list
context['mibs_path'] = mibs_path_list

ret = MSA_API.process_content('ENDED', 'Import OK', context, True)
print(ret)
