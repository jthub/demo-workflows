#!/usr/bin/env python

import os
import sys
import json
import subprocess
from utils import get_task_dict, save_output_json


task_dict = get_task_dict(sys.argv[1])

workdir = task_dict.get('input').get('workdir')
checker_wf_file_name = task_dict.get('input').get('checker_wf_file_name')
checker_job_file_name = task_dict.get('input').get('checker_job_file_name')

# link everything except for 'output.json' to the current working dir
for f in os.listdir(workdir):
    if f == 'output.json':
        continue
    os.symlink(os.path.join(workdir, f), f)

# TODO: we will need to modified the job json content in some cases where output
#       of the workflow file names are not fixed


try:
    subprocess.check_output(['cwltool', '--non-strict', checker_wf_file_name, checker_job_file_name])
except:
    with open('jt.log', 'w') as f:
        f.write("Workflow execution on '%s' failed." % checker_wf_file_name)

    output_json = { 'is_success': False }
    save_output_json(output_json)
    sys.exit(0)  # deliberately not to fail, pass to the next step to handle it

output_json = {
    'workdir': os.getcwd(),
    'is_success': True
}
save_output_json(output_json)
