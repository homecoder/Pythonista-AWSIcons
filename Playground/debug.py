# -*- coding: utf-8 -*-
import json

d = []
with open('debug.txt','r') as f:
    d = json.load(f)

for item in d:
    if 'nodes' in item:
        print(item['nodes'])
