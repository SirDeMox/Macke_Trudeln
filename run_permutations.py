import random as rd

import pandas as pd

# load results
df = pd.read_csv("early_stop_results_10k.csv")

# create lookup table to draw from
lookup_dict = {}
for index, row in df[["threshold", "games_n", ]].iterrows():
    thr = row["threshold"]
    gms = row["games_n"]
    if thr not in lookup_dict:
        lookup_dict[thr] = []
    lookup_dict[thr].append(gms)

# create all permutations
list1 = list(lookup_dict.keys())
permutations = []

for thr1 in list1:
    for thr2 in list1:
        permutation_tuple = (thr1, thr2)
        permutation_tuple_reversed = (thr2, thr1)
        if (permutation_tuple not in permutations) & (permutation_tuple_reversed not in permutations):
            permutations.append(permutation_tuple)

# run 5000 games
results_x = {}
results_y = {}

for i in range(5000):
    for thr1, thr2 in permutations:
        x = rd.sample(lookup_dict[thr1], 1)
        y = rd.sample(lookup_dict[thr2], 1)

        if not (thr1, thr2) in results_x:
            results_x[(thr1, thr2)] = []
        results_x[(thr1, thr2)].append(x > y)

        if not (thr1, thr2) in results_y:
            results_y[(thr1, thr2)] = []
        results_y[(thr1, thr2)].append(y > x)

# convert results into df
df_x = {res: sum(results_x[res]) / 1000 for res in results_x}
df_y = {res: sum(results_y[res]) / 1000 for res in results_y}
results_df_x = pd.DataFrame.from_dict(df_x, orient="index", columns=["win_rate_x"])
results_df_y = pd.DataFrame.from_dict(df_y, orient="index", columns=["win_rate_y"])

# merge and split tuples into columns
all_results = results_df_x.merge(results_df_y, left_index=True, right_index=True)
all_results["draw_rate"] = 1 - all_results.win_rate_x - all_results.win_rate_y
test = all_results.reset_index()
test.columns = ["thresholds", "win_rate_x", "win_rate_y", "draw_rate"]
test[["thr1", "thr2"]] = pd.DataFrame(test.thresholds.tolist(), index=test.index)

# save to csv
test.to_csv("results_5000_matches.csv")
