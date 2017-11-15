#!/usr/bin/env python

import os
import sys
import json
import subprocess
from utils import get_task_dict, save_output_json


task_dict = get_task_dict(sys.argv[1])

workdir = task_dict.get('input').get('workdir')
wf_file_name = task_dict.get('input').get('wf_file_name')
job_file_name = task_dict.get('input').get('job_file_name')

# link everything except for 'output.json' to the current working dir
for f in os.listdir(workdir):
    if f == 'output.json':
        continue
    os.symlink(os.path.join(workdir, f), f)

try:
    subprocess.check_output(['cwltool', '--non-strict', wf_file_name, job_file_name])
except:
    with open('jt.log', 'w') as f:
        f.write("Workflow execution on '%s' failed." % wf_file_name)
    sys.exit(1)

output_json = {
    'workdir': os.getcwd()
}

save_output_json(output_json)
