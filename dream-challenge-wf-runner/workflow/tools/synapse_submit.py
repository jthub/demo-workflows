#!/usr/bin/env python

import os
import sys
import shutil
import json
import subprocess
from utils import get_task_dict, save_output_json

synapse_conf_file = os.environ.get('SYNCONF')

task_dict = get_task_dict(sys.argv[1])

workflow_name = task_dict.get('input').get('workflow_name')
workdir = task_dict.get('input').get('workdir')
submit_job_file_name = task_dict.get('input').get('submit_job_file_name')
eval_id = task_dict.get('input').get('eval_id')
syn_parent_id = task_dict.get('input').get('syn_parent_id')
team_name = task_dict.get('input').get('team_name')

# copy everything except for 'output.json' to the current working dir
for f in os.listdir(workdir):
    if f == 'output.json':
        continue
    shutil.copytree(os.path.join(workdir, f), f)  # this is bad because it wastes a lot of space, but let's go with this for now

# get synapse-submit CWL file: dockstore-tool-synapse-submit.cwl (with a fixed id syn9732885)
subprocess.check_output(['synapse', '-c', synapse_conf_file, 'get', 'syn9732885'])

# TODO: we need to update the content of submit_job_file to include Team info, eval_id, parent_id etc
result_files = []
for f in os.listdir(os.getcwd()):
    if (f.startswith('HCC1143.csc_0-0-0.') and f.endswith('tar.gz')) or \
            f.startswith('run_id.embl-delly_1-3-0') or \
            f.startswith('SRR1198790.') or \
            f == '123e4567-e89b-12d3-a456-426655440000.db' or \
            f == 'md5sum.txt' or f == 'helloworld.txt':
        result_files.append({
            "path": f,
            "class": "File"
        })

submit_job = {
  "config_file": {
    "class": "File",
    "path": synapse_conf_file
  },
  "team_name": team_name,
  "eval_id": eval_id,
  "file": result_files,
  "parent_id": syn_parent_id
}

with open(os.path.join(os.getcwd(), submit_job_file_name), 'w') as f:
    f.write(json.dumps(submit_job))

try:
    subprocess.check_output(['cwltool', '--non-strict',
                             'dockstore-tool-synapse-submit.cwl', submit_job_file_name])
except:
    with open('jt.log', 'w') as f:
        f.write("Submission of workflow result on '%s' failed." % workflow_name)
    sys.exit(1)

output_json = {}
save_output_json(output_json)
