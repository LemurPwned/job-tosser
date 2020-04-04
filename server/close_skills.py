import pandas as pd
import ast
import numpy as np 
from sklearn.neighbors import DistanceMetric, NeighborhoodComponentsAnalysis
from sklearn.decomposition import NMF, FactorAnalysis
from collections import defaultdict
import json


class CloseSkills:
    def __init__(self):
        self.df = pd.read_csv('data/DATABASE.csv')
        self.df = self.df.drop('Unnamed: 0', axis=1)
        self.df['tag'] = self.df['Tags'].apply(self.filter_tags)
        self.build_matrix()

    def build_matrix(self):
        tag_dict = defaultdict(list)
        all_tags = self.df['tag'].tolist()

        flat_tags = [tag for tag_list in all_tags for tag in tag_list]
        self.flat_tag_dict = {tag: i for i, tag in enumerate(flat_tags)}
        self.inverted_tag_dict = {i: tag for i, tag in enumerate(flat_tags)}
        vectors = np.zeros(shape=(len(all_tags), len(flat_tags)), dtype=np.uint16)
        self.tag_matrix = np.zeros(shape=(len(flat_tags), len(flat_tags)), dtype=np.uint16)

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

    def filter_tags(self, str_tag_list):
        tag_list = ast.literal_eval(str_tag_list)
        return [x.strip() for x in tag_list]

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
        for i in range(size):
            ret[names[i]] = values[i]

        return json.dumps(ret)
        

if __name__ == "__main__":
    cs = CloseSkills()
    print(cs.perform_search("english"))
