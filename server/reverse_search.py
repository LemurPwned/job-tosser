import pandas as pd
import pickle
from collections import defaultdict, Counter, OrderedDict
import json


class ReverseSearch:
    def __init__(self):
        try:
            self.reverse_dict = pickle.load(open("reverse_dict2.pkl", "rb"))
        except:
            print("Unable to load pickle, generating...")
            self.prepare_db()

    def prepare_db(self):
        df = pickle.load(open("concat_db2.pkl", "rb"))
        reverse_dict = defaultdict(list)

        for _, row in df.iterrows():
            for tag in list(row['Tags']):
                reverse_dict[tag].append(row['Role'].replace("'", ""))

        for key in reverse_dict.keys():
            reverse_dict[key] = set(reverse_dict[key])

        pickle.dump(reverse_dict, open("reverse_dict2.pkl", "wb"))

    def perform_search(self, required, additional, limit=None):
        data = set(self.reverse_dict[required[0]])
        for word in required:
            temp = set(self.reverse_dict[word])
            data = data.intersection(temp)

        our_tags = set(additional)
        scores = []
        final_statistics = defaultdict(int)

        for role in data:
            final_statistics[role] = 0

        for tag in our_tags:
            tag_roles = self.reverse_dict[tag]
            for role in data:
                if role in tag_roles:
                    final_statistics[role] += 1

        final_roles = []
        for role in final_statistics:
            val = int(final_statistics[role] * 100 / len(additional))
            final_roles.append({
                'role': role,
                'percentage': val,
            })
        final_roles = sorted(final_roles,
                             key=lambda x: x['percentage'],
                             reverse=True)
        if limit and final_roles and (len(final_roles) > limit):
            final_roles = final_roles[:limit]
        return json.dumps(final_roles)


if __name__ == "__main__":
    rs = ReverseSearch()
    # rs.prepare_db()
    print(rs.perform_search(['java', 'javascript'], ['html']))
