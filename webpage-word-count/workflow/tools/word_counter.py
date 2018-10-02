#!/usr/bin/env python

import sys
import re
import time
from random import randint
from utils import get_task_dict, save_output_json

# sleep a random interval, purely for demo purpose
time.sleep(randint(5, 20))

task_dict = get_task_dict(sys.argv[1])

word = task_dict.get('input').get('word')
file_ = task_dict.get('input').get('file')

with open(file_, 'r') as f:
    webpage_html = f.read()

match_pattern = re.findall(r'\b{0}\b'.format(word), webpage_html, re.IGNORECASE)

output_json = {
    'count': len(match_pattern),
    'word': word
}

save_output_json(output_json)
