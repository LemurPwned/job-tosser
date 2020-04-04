import pandas as pd
import json
from collections import defaultdict

with open("output_1.txt") as f:
    data = f.read()
data = data.replace("][", ",")

print(data)
j = json.loads(data)

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
        all_keys.add(layer1)
        try:
            for layer2 in el[layer1].keys():
                all_keys.add(layer2)
                line[layer2] = el[layer1][layer2]
        except: 
            line[layer1] = el[layer1]
#print(line)

    for key in all_keys:
        if key in ["whole_unnormalized_body", "job_description_details"]:
            continue
        csv_data += '"' + str(line[key]) + '",'
    csv_data += "\n"
with open("fb.csv", "w+") as f:
    f.write(csv_data)





