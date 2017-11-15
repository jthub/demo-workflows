#!/usr/bin/env python

import os
import sys
from utils import get_task_dict, save_output_json

task_dict = get_task_dict(sys.argv[1])

workdir = task_dict.get('input').get('workdir')
submit_job_file_name = task_dict.get('input').get('submit_job_file_name')
eval_id = task_dict.get('input').get('eval_id')
syn_parent_id = task_dict.get('input').get('syn_parent_id')
team_name = task_dict.get('input').get('team_name')

# link everything except for 'output.json' to the current working dir
for f in os.listdir(workdir):
    if f == 'output.json':
        continue
    os.symlink(os.path.join(workdir, f), f)

# get synapse-submit CWL file: dockstore-tool-synapse-submit.cwl (with a fixed id syn9732885)
subprocess.check_output(['synapse', '-c', synapse_conf_file, 'get', 'syn9732885'])

# TODO: we need to update the content of submit_job_file to include Team info, eval_id, parent_id etc

#try:
#    subprocess.check_output(['cwltool', '--non-strict',
#                             'dockstore-tool-synapse-submit.cwl', submit_job_file_name])
#except:
#    with open('jt.log', 'w') as f:
#        f.write("Submission of workflow result on '%s' failed." % workflow_name)
#    sys.exit(1)

output_json = {}
save_output_json(output_json)
