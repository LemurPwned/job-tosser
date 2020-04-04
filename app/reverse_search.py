import json
import pickle
from collections import Counter, OrderedDict, defaultdict

import pandas as pd
import os

REVERSE_SEARCH_DICT = 'reverse_search.pkl'


class ReverseSearch:
    def __init__(self, DATABASE):
        self.reverse_dict = {}
        # if os.path.isfile(REVERSE_SEARCH_DICT):
        #     self.reverse_dict = pickle.load(open(DATABASE, "rb"))
        # else:
        #     self.reverse_dict = self.prepare_db(DATABASE)
        # print("REVERSE DATABASE loaded!")

    def prepare_db(self, db):
        df = pickle.load(open(db, "rb"))
        reverse_dict = defaultdict(list)

        for _, row in df.iterrows():
            for tag in list(row['Tags']):
                reverse_dict[tag].append(row['Role'].replace("'", ""))

        for key in reverse_dict.keys():
            reverse_dict[key] = set(reverse_dict[key])
        pickle.dump(reverse_dict, open(REVERSE_SEARCH_DICT, "wb"))
        return reverse_dict

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
