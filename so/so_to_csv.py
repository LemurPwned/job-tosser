import pickle
import pandas as pd

keys_all = ['Job type', 'Experience level', 'Role', 'Industry', 'Company size', 'Company type', 'Salary', 'Remote', 'Location']

data = pickle.load(open("so.pkl", "rb"))

str_data = "job_type,experience,role,industry,company_size,company_type,salary,remote,location,tags\n"
for row in data:
    for key in keys_all:
        str_data += '"' + str(row[1][key]) + '"' + ","
    str_data += '"' + str(row[0]) + "\"\n"

with open("so.csv", "w") as f:
    f.write(str_data)

df = pd.read_csv("so.csv", sep=",")
print(df.head())
print(df.describe())
df = df[df['role'] != "None"]
df.drop_duplicates(inplace=True)
print(df.describe())
df.to_csv("so.csv", index=False)

