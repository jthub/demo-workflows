#!/usr/bin/env python

import os
import sys
import time
import urllib2
from random import randint
from utils import get_task_dict, save_output_json

# sleep a random interval, purely for demo purpose
time.sleep(randint(5, 10))

task_dict = get_task_dict(sys.argv[1])

# download from the url
url = task_dict.get('input').get('url')
response = urllib2.urlopen(url)

# write to a file
file_name = '%s.html' % int(time.time())
with open(file_name, 'w') as f:
    f.write(response.read())

output_json = {
    'file': os.path.join(os.getcwd(), file_name)
}

save_output_json(output_json)
