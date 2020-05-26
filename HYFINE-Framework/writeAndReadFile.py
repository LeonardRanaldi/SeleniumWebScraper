# -*- coding: utf-8 -*-
import collections
from collections import defaultdict
#import simplejson as json
import json  # using stdlib module instead



def writeFile(p, nome):

    json_data = json.dumps(p, indent=2)
    json.dump(p, open('/path/'+nome+'.json', 'a+'), indent=2)
    print(json_data)


#read from file and print results
def readFile(nome):

    d = collections.defaultdict(dict)
    with open(nome) as f:
        d = json.load(f)
    json_data = json.dumps(d, indent=2)
    print(json_data)
    print(type(d))
    return d

#read from file
def readFileNOprint(nome):

    d = collections.defaultdict(dict)
    with open(nome) as f:
        d = json.load(f)

    return d


