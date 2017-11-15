#!/usr/bin/env python

import os
import sys
import json
import subprocess
from utils import get_task_dict, save_output_json

synapse_conf_file = os.environ.get('SYNCONF')

task_dict = get_task_dict(sys.argv[1])

workflow_name = task_dict.get('input').get('workflow_name')

# hardcode this mapping here
synapse_ids = {
    'pcawg-sanger-variant-caller': [
        'syn10517387',
        'pcawg-sanger-variant-caller.cwl',
        'pcawg-sanger-variant-caller.job.json',
        'pcawg-sanger-variant-caller.checker.cwl',
        'pcawg-sanger-variant-caller.checker.job.json',
        'pcawg-sanger-variant-caller.submit.json'
    ],
    'pcawg-bwa-mem-aligner': [
        'syn10517407',
        'pcawg-bwa-mem-aligner.cwl',
        'pcawg-bwa-mem-aligner.json',
        'pcawg-bwa-mem-aligner.checker.cwl',
        'pcawg-bwa-mem-aligner.checker.job.json',
        'pcawg-bwa-mem-aligner.submit.json'  # this name needs to be verified
    ],
    'pcawg-delly-sv-caller': [
        'syn10793418',
        'pcawg-delly-sv-caller.cwl',
        'pcawg-delly-sv-caller.cwl.json',
        'pcawg-delly-sv-caller_checker.cwl',
        'pcawg-delly-sv-caller_checker.cwl.json',
        'pcawg-delly-sv-caller_submit.cwl.json'
    ]
}

eval_ids = {
  'md5sum' = '9603664',
  'hello_world' = '9603665',
  'biowardrobe_chipseq_se' = '9604287',
  'gdc_dnaseq_transform' = '9604596',
  'bcbio_NA12878-chr20' = '9605240',
  'encode_mapping_workflow' = '9605639',
  'knoweng_gene_prioritization' = '9606345',
  'pcawg-delly-sv-caller' = '9606704',
  'pcawg-sanger-variant-caller' = '9606705',
  'pcawg-broad-variant-caller' = '9606714',
  'pcawg-bwa-mem-aligner' = '9606715',
  'pcawg-dkfz-variant-caller' = '9606716',
  'bcbio-giab-joint' = '9606717',
  'broad-gatk-data-processing' = '9607589'
  'broad-gatk-validate-bam' = '9607590'
}

workflow_data_target_folder = synapse_ids.get(workflow_name)[0]

if not workflow_data_target_folder:
    with open('jt.log', 'w') as f:
        f.write("Specified challenge workflow '%s' does not exist." % workflow_name)
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
# get synapse-submit CWL file: dockstore-tool-synapse-submit.cwl (with a fixed id syn9732885)
subprocess.check_output(['synapse', '-c', synapse_conf_file, 'get', 'syn9732885'])

# run synapse get tool
subprocess.check_output(['cwltool', '--non-strict', 'dockstore-tool-synapse-get.cwl', 'stage-files.json'])

output_json = {
    'workflow_name': workflow_name,
    'workdir': os.getcwd(),
    'cwl_file_name': synapse_ids.get(workflow_name)[1],
    'job_file_name': synapse_ids.get(workflow_name)[2],
    'checker_cwl_file_name': synapse_ids.get(workflow_name)[3],
    'checker_job_file_name': synapse_ids.get(workflow_name)[4],
    'submit_job_file_name': synapse_ids.get(workflow_name)[5],
    'eval_id': eval_ids.get(workflow_name)
}

save_output_json(output_json)
