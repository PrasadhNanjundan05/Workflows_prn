import os
import subprocess
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
mibs_name_list = {}

oid_startswith_filter_list = ('0.')

imported_mib = ''
imported_mib_nb = 0
imported_oid_list = {}

'''
Get the list of the MIB names and the list of the path where MIBs are located
    Walk through the mib_path_root_list recursively
    For each file having an extension name in extention_mib_file_list
    get the MIB name and save the result in a dictionary mibs_name_list
    except for standard mibs (standard_mibs_path)
    Path where MIBs are located are stored in the dictionary mibs_path_list
'''
pattern = '^\s*([^\s]+)\s+DEFINITIONS\s+::= BEGIN'
regc = re.compile(pattern)
def build_mib_mapping(mibs_name_list, dirpath, fname):
    mib_file = dirpath + os.path.sep + fname
    with open(mib_file, 'r') as f:
        for line in f:
            result = regc.search(line)
            if result != None:
                mib_name = result.group(1)
                mibs_name_list[mib_name] = fname
                break
    return mibs_name_list

'''
Convert mibs_name_list dictionary in list for UI
'''
mib_name = []

context['mib_name'] = 

for mib_path in mibs_path_root_list:
    for dirpath, dirs, files in os.walk(mib_path):
        for fname in files:
            if fname.endswith(extention_mib_file_list):
                if mib_path != standard_mibs_path:
                    mibs_name_list = build_mib_mapping(mibs_name_list, dirpath, fname)
                if not dirpath in mibs_path_list:
                    mibs_path_list[dirpath] = True

if not mibs_name_list:
    context['imported_oids'] = imported_oid_list
    context['import_summary'] = f'Total {imported_mib_nb} : {imported_mib}'
    ret = MSA_API.process_content('ENDED', 'No MIB to import', context, True)
    print(ret)

'''
Parse the MIBs
    Translate OID names in OIDs thanks to snmptranslate CLI
    Build the dictionary oid_list with key = oid, value = oid name
    to ensure the uniqueness of the oid
'''
oid_list = {}
mib_path_str = ':'.join(mibs_path_list)
mib_name_str = ':'.join(mibs_name_list)
cmd = ['/usr/bin/snmptranslate', '-Pu', '-Tz', '-M', mib_path_str, '-m', mib_name_str]
# for python >= 3.7 replace universal_newlines by text
proc = subprocess.run(cmd, stdout = subprocess.PIPE, stderr = subprocess.STDOUT, universal_newlines = True)
if proc.returncode == 0:
    # each line of out is like "oid name" "oid"
    out = proc.stdout
    pattern = '^\s*"([^"]+)"\s+"([^"]+)"'
    regc = re.compile(pattern, flags = re.MULTILINE)
    result = regc.findall(out)
    if result != None:
        # result is a list of tuple, each tuple is a (oid_name, oid) pair
        for name, oid in result:
            if not oid.startswith(oid_startswith_filter_list):
                if not oid in oid_list:
                    oid_list[oid] = name

'''
Build a tree  in the dictionary oid_tree to identify leaves
'''
oid_tree = {}
def add_node(tree, oid, name):
    new_tree = cur_tree = tree
    for item in oid.split('.'):
        if item not in cur_tree:
            cur_tree[item] = {}
        cur_tree = cur_tree[item]
    return new_tree

for oid, name in oid_list.items():
    oid_tree = add_node(oid_tree, oid, name)

'''
Get leaves from the tree oid_tree
and store them in a dictionary
'''
leaf_list= {}
oid = ''
def get_leaves(tree, oid, leaves):
    cur_oid = oid
    cur_leaves = leaves
    for key, value in tree.items():
        if oid:
            cur_oid = oid + '.' + key
        else:
            cur_oid = key
        if value:
            cur_leaves = get_leaves(value, cur_oid, cur_leaves)
        else:
            cur_leaves[cur_oid] = True
    return cur_leaves

leaf_list = get_leaves(oid_tree, oid, leaf_list)

'''
Build a new dictionary for the WF task
with leaves only
'''
imported_oid_list = []
for oid, name in oid_list.items():
    if oid in leaf_list:
        imported_oid_list.append({'oid': oid, 'oid_name': name, 'selected': False})

context['imported_oids'] = imported_oid_list

imported_mib = ', '.join(mibs_name_list)
imported_mib_nb = len(mibs_name_list)
context['import_summary'] = f'Total {imported_mib_nb} : {imported_mib}'

ret = MSA_API.process_content('ENDED', 'Import OK', context, True)
print(ret)

