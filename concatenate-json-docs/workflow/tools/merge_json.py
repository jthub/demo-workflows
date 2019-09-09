#!/usr/bin/env python

import os
import sys
import json

cwd = os.getcwd()

task_dict = json.loads(sys.argv[1])


files = task_dict.get('input').get('json_docs')

with open('merged_doc.jsonl', 'w') as o:
    for f in files:
        with open(f, 'r') as d:
            json_doc = json.load(d)
        o.write(json.dumps(json_doc))


output_json = {
    'merged_doc': os.path.join(cwd, 'merged_doc.jsonl')
}

with open('output.json', 'w') as o:
    o.write(json.dumps(output_json, indent=2))
