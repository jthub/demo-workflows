#!/usr/bin/env python

import sys
import re
from utils import get_task_dict, save_output_json

task_dict = get_task_dict(sys.argv[1])

word = task_dict.get('input').get('word')
file_ = task_dict.get('input').get('file')

with open(file_, 'r') as f:
    webpage_html = f.read()

match_pattern = re.findall(r'\b{0}\b'.format(word), webpage_html)

output_json = {
    'count': len(match_pattern),
    'word': word
}

save_output_json(output_json)
