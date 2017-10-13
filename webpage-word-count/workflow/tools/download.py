#!/usr/bin/env python

import os
import sys
import requests
import time
from utils import get_task_dict, save_output_json

task_dict = get_task_dict(sys.argv[1])

# download from the url
url = task_dict.get('url')
response = requests.get(url)

# write to a file
file_name = '%s.html' % int(time.time())
with open(file_name, 'w') as f:
    f.write(response.content)

output_json = {
    'file': os.path.join(cwd, file_name)
}

save_output_json(output_json)
