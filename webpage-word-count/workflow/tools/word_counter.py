#!/usr/bin/env python

import re
import bs4
from utils import get_task_dict, save_output_json

task_dict = get_task_dict(sys.argv[1])

word = task_dict.get('word')
file_ = task_dict.get('file')

with open(file_, 'r') as f
    webpage_html = f.read()

soup = bs4.BeautifulSoup(webpage_html, 'html.parser')
results = soup.body.find_all(string=re.compile('.*{0}.*'.format(word)), recursive=True)

output_json = {
    'count': len(results)
}

save_output_json(output_json)
