import ast
import json
import os
import re
from collections import Counter, defaultdict

import numpy as np
import pandas as pd


def term_in_doc(t, d):
    if t in d:
        return True
    else:
        return False


def calc_tfidf(t, d, D):
    """
    All specific role create a document    
    """
    freqs = [D[role][t] for role in D]
    tmax = max(freqs)
    tf = 0.5 + \
        0.5*d[t]/tmax
    x = [term_in_doc(t, D[role]) for role in D]
    idf = np.log(len(d) / sum(x))
    return tf * idf


class Aggregator:
    synonyms = [("developer", "engineer")]
    forced = ["C", "java"]

    def __init__(self, database):
        self.db = pd.read_pickle(database)
        self.unique_roles = self.db['Role'].unique()
        self.role_tfidf = self.create_documents_counts(self.db)

    def replace_with_synonyms(self, role):
        for i in Aggregator.synonyms:
            for word in role.split(' '):
                if word in str(i):
                    role = role.replace(word, f"({'|'.join(i)})")

        return role

    def force_boundaries(self, role):
        for word in role.split(' '):
            if word in Aggregator.forced:
                role = role.replace(word, f"\\b{word}\\b")

        return role

    def preprocess_role(self, role):
        role = role.replace("+", "\+")
        role = self.replace_with_synonyms(role)
        role = self.force_boundaries(role)
        return role

    def find_coocurring(self, skill):
        """
        Find most frequently coocurring skills
        """
        skill = skill.replace("+", "\+")
        skill = self.force_boundaries(skill)
        rows_containing = self.db.loc[self.db['Tags'].astype(str).str.contains(
            skill, flags=re.IGNORECASE, regex=True)]
        flattened = []
        for offer in rows_containing['Tags'].values:
            flattened.extend(offer)

        c = Counter(flattened)
        final_statistics = []
        for k, v in c.most_common(10):
            to_cmp = k.replace("+", "\+")
            to_cmp = self.force_boundaries(to_cmp)
            if to_cmp != skill:
                final_statistics.append({
                    'name':
                    k,
                    'result':
                    int(v / len(rows_containing) * 100)
                })
        return json.dumps(final_statistics)

    def search_in_db(self, role, limit=None):
        """
        Return statistics for a role from a db 
        """
        role = self.preprocess_role(role)
        new_roles = self.db.loc[self.db['Role'].str.contains(
            role, flags=re.IGNORECASE, regex=True)]

        all_tags = new_roles['Tags'].to_numpy()
        # flatten all tags
        if all_tags.any():
            flat_tags = np.concatenate(all_tags).ravel()
            c = Counter(flat_tags)
            final_statistics = [{"unique": len(new_roles)}]
            for k, v in c.most_common(limit):
                final_statistics.append({
                    'skill':
                    k,
                    'count':
                    v,
                    'percentage':
                    int(v * 100 / len(new_roles))
                })
            return json.dumps(final_statistics)
        else:
            return json.dumps("")

    def create_documents_counts(self, df):
        global_counts = Counter()
        role_counts = {}
        for role in df['Role'].unique():
            if not role:
                continue
            skillset = df['Tags'].loc[df['Role'] == role].to_numpy()
            # flatten all tags
            flat_tags = np.concatenate(skillset).ravel()
            tcount = Counter(flat_tags)
            global_counts += tcount
            if role not in role_counts:
                role_counts[role] = Counter()
            role_counts[role] += tcount

        tfidf_role = {}
        for role in df['Role'].unique():
            if not role:
                continue
            tfidf_role[role] = Counter()
            skillset = df['Tags'].loc[df['Role'] == role].to_numpy()
            flat_tags = np.concatenate(skillset).ravel()
            # print(f"Role {role}")
            for skill in flat_tags:
                score = calc_tfidf(skill, role_counts[role], role_counts)
                # print(f"\t{skill}: {score}")
                tfidf_role[role][skill] = score

        return tfidf_role

    def query_role_tfidf(self, role, limit=None):
        try:
            idfs = self.role_tfidf[role]
            vals = [v for k, v in idfs.items()]
            offset = abs(min(vals))
            total = sum(vals)
            res = sorted([(skill, (100 * (val + offset) / total))
                          for skill, val in idfs.items()], lambda x: x[1])
            if limit and final_roles and (len(final_roles) > limit):
                return res[:limit]
            else:
                return res
        except:
            return json.dumps(None)


if __name__ == '__main__':
    ag = Aggregator()
    # ag.build_statistics()
    print(ag.search_in_db('Data *', 10))
