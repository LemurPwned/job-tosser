import pandas as pd
import json
from collections import defaultdict
import codecs
import sys

f = sys.argv[1]

#with open(f) as f:
    #data = f.read()

#print(data)
j = json.load(codecs.open(f, 'r', 'utf-8-sig'))

all_keys = set()

for el in j:
    for layer1 in el.keys():
        all_keys.add(layer1)
        try:
            for layer2 in el[layer1].keys():
                all_keys.add(layer2)
        except: pass

csv_data = ""
for key in all_keys:
    if key in ["whole_unnormalized_body", "job_description_details"]:
        continue
    csv_data += '"' + key + "\","
csv_data = csv_data[:-1]
csv_data += "\n"

line = defaultdict(lambda: "None")
for el in j:
    for layer1 in el.keys():
        try:
            for layer2 in el[layer1].keys():
                line[layer2] = el[layer1][layer2]
        except: 
            line[layer1] = el[layer1]
#print(line)

    for key in all_keys:
        if key in ["whole_unnormalized_body", "job_description_details"]:
            continue
        csv_data += '"' + str(line[key]) + '",'
    csv_data += "\n"
name = sys.argv[1].split(".")[0]


with open(name + ".csv", "w+") as f:
    f.write(csv_data)
