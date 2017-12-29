#!/usr/bin/env python

import os
import sys
import re
import shutil
import json
import subprocess
from utils import get_task_dict, save_output_json


task_dict = get_task_dict(sys.argv[1])

workdir = task_dict.get('input').get('workdir')
workflow_name = task_dict.get('input').get('workflow_name')
checker_wf_file_name = task_dict.get('input').get('checker_wf_file_name')
checker_job_file_name = task_dict.get('input').get('checker_job_file_name')

# copy everything except for 'output.json' to the current working dir
for f in os.listdir(workdir):
    if f == 'output.json':
        continue
    if os.path.isdir(os.path.join(workdir, f)):
        shutil.copytree(os.path.join(workdir, f), f)  # this is bad because it wastes a lot of space, but let's go with this for now
    else:
        shutil.copy(os.path.join(workdir, f), f)

# TODO: we will need to modified the job json content in some cases where output
#       of the workflow file names are not fixed
if workflow_name == 'pcawg-sanger-variant-caller' or \
   workflow_name == 'encode_mapping_workflow':
    result_files = []
    for f in os.listdir(os.getcwd()):
        if f.startswith('HCC1143.csc_0-0-0.') and f.endswith('tar.gz'):
            result_files.append({
                "path": f,
                "class": "File"
            })
        elif re.match(r'[0-9]+-[0-9]+-20[0-9]{2}T[0-9]+H[0-9]+M[0-9]+S', f):
            result_files.append({
                "path": f,
                "class": "Directory"
            })

    with open(os.path.join(os.getcwd(), checker_job_file_name), 'r') as f:
        checker_job = json.load(f)

    checker_job['result_files'] = result_files
    with open(os.path.join(os.getcwd(), checker_job_file_name), 'w') as f:
        f.write(json.dumps(checker_job))

try:
    subprocess.check_output(['cwltool', '--non-strict', checker_wf_file_name, checker_job_file_name])
except:
    with open('jt.log', 'w') as f:
        f.write("Workflow execution on '%s' failed." % checker_wf_file_name)

    output_json = { 'is_success': False }
    save_output_json(output_json)
    sys.exit(1)

output_json = {
    'workdir': os.getcwd(),
    'is_success': True
}
save_output_json(output_json)

