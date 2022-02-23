import os
import subprocess
import re

from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('import_mibs_path', var_type='String')

context = Variables.task_call(dev_var)
import_mibs_path = context['import_mibs_path']

mibs_path_root_list = ['/usr/share/snmp/mibs', import_mibs_path]
mibs_path_list = {} # use a dictionary to have each path once

extention_mib_file_list = ('.txt')
mib_name_list = {}

'''
Get the list of the MIB names
    walk through the mib_path_list recursively
    for each file having an extension name in extention_mib_file_list
    get the MIB name and save the result in a dictionary mib_name_list
'''
pattern = '^\s*([^\s]+)\s+DEFINITIONS\s+::= BEGIN'
regc = re.compile(pattern)
def build_mib_mapping(mib_name_list, dirpath, fname):
    mib_file = dirpath + os.path.sep + fname
    with open(mib_file, 'r') as f:
        for line in f:
            result = regc.search(line)
            if result != None:
                mib_name = result.group(1)
                mib_name_list[mib_name] = fname
                break
    return mib_name_list

for mib_path in mibs_path_root_list:
    for dirpath, dirs, files in os.walk(mib_path):
        for fname in files:
            if fname.endswith(extention_mib_file_list):
                mib_name_list = build_mib_mapping(mib_name_list, dirpath, fname)
                if not dirpath in mibs_path_list:
                    mibs_path_list[dirpath] = True

'''
Parse the MIBs
    translate OID names in OIDs thanks to snmptranslate CLI
    build the dictionary oid_list with key = oid, value = oid name
'''
oid_list = {}
mib_path_str = ':'.join(mibs_path_list)
mib_name_str = ':'.join(mib_name_list)
cmd = ['/usr/bin/snmptranslate', '-Pu', '-Tz', '-M', mib_path_str, '-m', mib_name_str]
# for python >= 3.7 replace universal_newlines by text
proc = subprocess.run(cmd, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, universal_newlines = True)
if proc.returncode == 0:
    out = proc.stdout
    pattern = '^\s*"([^"]+)"\s+"([^"]+)"'
    regc = re.compile(pattern, flags = re.MULTILINE)
    # each line of out is like "oid name" "oid"
    result = regc.findall(out)
    if result != None:
        # result is a list of tuple, each tuple is a (oid_name, oid) pair
        for name, oid in result:
            if not oid in oid_list:
                oid_list[oid] = name

ret = MSA_API.process_content('ENDED', f'Import OK\n{oid_list}', context, True)
print(ret)

