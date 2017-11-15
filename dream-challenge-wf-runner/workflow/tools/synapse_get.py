#!/usr/bin/env python

import os
import sys
import json
import subprocess
from utils import get_task_dict, save_output_json

synapse_conf_file = os.environ.get('SYNCONF')

task_dict = get_task_dict(sys.argv[1])

workflow_name = task_dict.get('input').get('workflow_name')
workflow_data_target_folder = task_dict.get('input').get('data_syn_id')

if not workflow_data_target_folder:
    with open('jt.log', 'w') as f:
        f.write("Specified challenge workflow data Synapse ID '%s' does not exist." \
                % workflow_data_target_folder)
    sys.exit(1)  # task failed

synapse_get_job = {
    "config_file": {
        "class": "File",
        "path": synapse_conf_file
    },
    "synapse_id": workflow_data_target_folder,
    "recursive": True
}

# now safe the job file to JSON file
with open('stage-files.json', 'w') as f:
    f.write(json.dumps(synapse_get_job))

# get synapse-get CWL file: dockstore-tool-synapse-get.cwl (with a fixed id syn9770802)
subprocess.check_output(['synapse', '-c', synapse_conf_file, 'get', 'syn9770802'])

# run synapse get tool
subprocess.check_output(['cwltool', '--non-strict', 'dockstore-tool-synapse-get.cwl', 'stage-files.json'])

output_json = {
    'workdir': os.getcwd()
}

save_output_json(output_json)
