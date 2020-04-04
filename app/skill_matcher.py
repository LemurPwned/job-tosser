import ast
import json
import os
import pickle
from collections import defaultdict

import numpy as np
import pandas as pd

LOCAL_MATRIX = 'matrix.npy'
LOCAL_FLAT_TAG = 'local_flat_tag.pkl'
LOCAL_INV_TAG = 'local_inv_tag.pkl'


class SkillMatcher:
    def __init__(self, database=None):
        self.df = pd.read_csv(database)
        self.df['Tags'] = self.df['Tags'].apply(self.filter_tags)
        if os.path.isfile(LOCAL_MATRIX) and os.path.isfile(
                LOCAL_INV_TAG) and os.path.isfile(LOCAL_FLAT_TAG):
            self.tag_matrix = np.load(LOCAL_MATRIX)
            self.flat_tag_dict = pickle.load(open(LOCAL_FLAT_TAG, 'rb'))
            self.inverted_tag_dict = pickle.load(open(LOCAL_INV_TAG, 'rb'))
        else:
            if not database:
                raise ValueError("EMPTY DB LOC!")
            self.build_matrix()
        print("Loaded the data!")

    def build_matrix(self):
        tag_dict = defaultdict(list)
        all_tags = self.df['Tags'].tolist()

        flat_tags = [tag for tag_list in all_tags for tag in tag_list]
        self.flat_tag_dict = {tag: i for i, tag in enumerate(flat_tags)}
        self.inverted_tag_dict = {i: tag for i, tag in enumerate(flat_tags)}
        vectors = np.zeros(shape=(len(all_tags), len(flat_tags)),
                           dtype=np.uint16)
        self.tag_matrix = np.zeros(shape=(len(flat_tags), len(flat_tags)),
                                   dtype=np.uint16)

        for k, tag_list in enumerate(all_tags):
            for i in range(len(tag_list)):
                i_tag = self.flat_tag_dict[tag_list[i]]
                vectors[k][i] = 1
                for j in range(len(tag_list)):
                    if i == j:
                        continue
                    j_tag = self.flat_tag_dict[tag_list[j]]
                    self.tag_matrix[i_tag, j_tag] += 1
                    self.tag_matrix[j_tag, i_tag] += 1
        np.save(LOCAL_MATRIX, self.tag_matrix)
        pickle.dump(self.flat_tag_dict, open(LOCAL_FLAT_TAG, 'wb'))
        pickle.dump(self.inverted_tag_dict, open(LOCAL_INV_TAG, 'wb'))

    def filter_tags(self, str_tag_list):
        tag_list = ast.literal_eval(str_tag_list)
        return [x.strip() for x in tag_list]

    def query_salary_per_skills(self,
                                skill_list,
                                quantiles=[0.25, 0.5, 0.75, 1.0]):
        """
        Return the quantiles for a set of skills 
        """
        skills_in_df_mask = self.df['Tags'].apply(
            lambda x: set(skill_list).issubset(x))
        skills_in = self.df[skills_in_df_mask]
        # exclude zero stuff
        skills_in = skills_in.loc[(skills_in['Min_Annual_Eur_Salary'] > 0)
                                  & (skills_in['Max_Annual_Eur_Salary'] > 0)]

        min_quantiles = skills_in['Min_Annual_Eur_Salary'].quantile(
            quantiles).tolist()
        max_quantiles = skills_in['Max_Annual_Eur_Salary'].quantile(
            quantiles).tolist()

        avg_min = skills_in['Min_Annual_Eur_Salary'].mean()
        avg_max = skills_in['Max_Annual_Eur_Salary'].mean()

        return_json = {
            'min_quantiles': min_quantiles,
            'max_quantiles': max_quantiles,
            'avg_min': avg_min,
            'avg_max': avg_max
        }
        print(return_json)
        return json.dumps(return_json)

    def perform_search(self, tag, size=5):
        """
        Returns the indices and the values 
        """
        tag_id = self.flat_tag_dict[tag]
        skill_indices_n = self.tag_matrix[tag_id, :].argsort()[::-1][:size]
        skill_vals = self.tag_matrix[tag_id, skill_indices_n]

        ret = {}
        names = [self.inverted_tag_dict[ind] for ind in skill_indices_n]
        values = [int(i) for i in skill_vals]
        res_list = []
        sum_vals = sum(values)
        for i in range(size):
            res_list.append({
                'skill': names[i],
                'count': values[i],
                'percentage': int(100 * values[i] / sum_vals)
            })
        return json.dumps(res_list)


if __name__ == "__main__":
    cs = SkillMatcher('../data/DATABASE.csv')
    print(cs.perform_search("english"))
