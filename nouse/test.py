#!/usr/bin/python
import json

jsonData = '{"a":1,"b":2,"c":3,"d":4,"e":5}';
if 'a' in jsonData:
    print 'lalala'
text = json.loads(jsonData)
print text