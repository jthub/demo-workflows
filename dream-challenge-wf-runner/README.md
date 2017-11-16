# JTracker Demo Workflow: dream-challenge-workflow-runner

Note: this is a quick draft with major components in place to run GA4GH Dream Challenge Workflows.


## Example Job Files

Example Job files can be found in `example_jobs` directory.


## Enqueue Jobs

Enqueue job can be done on any computer.

```
# assume job queue ID: e99983c7-378f-429c-81ba-68849ab3dcda
jt job add -q  e99983c7-378f-429c-81ba-68849ab3dcda -j '
{
    "workflow_name": "pcawg-sanger-variant-caller",
    "workflow_type": "CWL",
    "data_syn_id": "syn10517387",
    "wf_file_name": "pcawg-sanger-variant-caller.cwl",
    "job_file_name": "pcawg-sanger-variant-caller.job.json",
    "checker_wf_file_name": "pcawg-sanger-variant-caller.checker.cwl",
    "checker_job_file_name": "pcawg-sanger-variant-caller.checker.job.json",
    "submit_job_file_name": "pcawg-sanger-variant-caller.submit.json",
    "team_name": "PCAWG-Tech",
    "syn_parent_id": "syn11449436",
    "eval_id": "9606705"
}'
```

## Run Jobs
Compute node runs JTracker executor needs to have `cwltool` and `docker` installed.

```
# environment variable for Synapse config file needs to set properly
SYNCONF=/home/ubuntu/.synapseConfig jt exec run -q e99983c7-378f-429c-81ba-68849ab3dcda
```
