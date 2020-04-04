import pickle

keys_all = ['Job type', 'Experience level', 'Role', 'Industry', 'Company size', 'Company type']

data = pickle.load(open("so.pkl", "rb"))

str_data = "job_type,experience,role,industry,company_size,company_tipe,tags\n"
for row in data:
    for key in keys_all:
        str_data += str(row[1][key]) + ","
    str_data += str(row[0]) + "\n"

with open("so.csv", "w") as f:
    f.write(str_data)
        
