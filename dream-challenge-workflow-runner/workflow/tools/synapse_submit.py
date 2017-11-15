#!/usr/bin/env python

import os
import sys
from utils import get_task_dict, save_output_json

task_dict = get_task_dict(sys.argv[1])

workdir = task_dict.get('input').get('workdir')
workflow_name = task_dict.get('input').get('workflow_name')
submit_job_file_name = task_dict.get('input').get('submit_job_file_name')
eval_id = task_dict.get('input').get('eval_id')

# link everything except for 'output.json' to the current working dir
for f in os.listdir(workdir):
    if f == 'output.json':
        continue
    os.symlink(os.path.join(workdir, f), f)


try:
    subprocess.check_output(['cwltool', '--non-strict', cwl_file_name, job_json_name])
except:
    with open('jt.log', 'w') as f:
        f.write("Submission of workflow result on '%s' failed." % workflow_name)
    sys.exit(1)

output_json = {
    'workflow_name': workflow_name
}
save_output_json(output_json)
