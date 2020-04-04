def get_experience_count_by_technologies(db):
    """
    data dict schema
    data = {'technology': {'experience_lvl': 'count'}} for each technology
    """

    df = db.groupby(['Experience']).agg({'Tags': 'sum'}).reset_index()
    data = {}

    def _sum_experiences(exp, tags):
        for tag in tags:
            lvls = {
                'Junior': 0,
                'Mid-Level': 0,
                'Senior': 0,
                'Lead': 0,
                'Manager': 0
            }
            data.setdefault(tag, lvls)
            for key in lvls.keys():
                if key in exp:
                    data[tag][key] += 1

    [_sum_experiences(exp, tags) for exp, tags in zip(df['Experience'], df['Tags'])]
    return data
